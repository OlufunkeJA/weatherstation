<template>
    <div class="chart-container">
      <h3>Live {{ selectedChartMetric.charAt(0).toUpperCase() + selectedChartMetric.slice(1) }} Graph</h3>

      <div class="chart-metric-selector">
        <label for="chartMetric" class = "label">Show Live Graph For: </label>
        <select id="chartMetric" v-model="selectedChartMetric">
          <option value="temperature">Temperature</option>
          <option value="humidity">Humidity</option>
          <option value="pressure">Pressure</option>
          <option value="heatindex">Heat Index</option>
          <option value="moisture">Moisture</option>
          <option value="altitude">Altitude</option>
        </select>
      </div>

      <LineChart v-if="chartData.labels && chartData.labels.length > 1" :chart-data="chartData"
        :chart-options="chartOptions" />
      <p v-else>Collecting data...</p>
    </div>
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS
import { ref, reactive, watch, onMounted, onBeforeUnmount, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useMqttStore } from '@/store/mqttStore';
import { useAppStore } from "@/store/appStore";
import { storeToRefs } from "pinia";
const Mqtt = useMqttStore();
const { payload, payloadTopic } = storeToRefs(Mqtt);

import LineChart from '@/components/LineChart.vue'; // Import chart component
const units = ref('metric'); // 'metric' or 'imperial'
const selectedChartMetric = ref('temperature'); // Default metric for the chart



// VARIABLES
const router = useRouter();
const route = useRoute();
const tempHiChart = ref(null); // Chart object
const humidHiChart = ref(null); // Chart object
const points = ref(10); // Specify the quantity of points to be shown on the live graph simultaneously.
const shift = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.

// FUNCTIONS
onMounted(() => {
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED

    Mqtt.connect(); // Connect to Broker located on the backend
    setTimeout(() => {
        // Subscribe to each topic
        Mqtt.subscribe("620162688");
        //Mqtt.subscribe("topic2");
    }, 3000);

    /*const ctx = document.querySelector('#chart'); // Select canvas for rendering chart
    chart = new Chart(ctx, config ); // create chart

    const ctx1 = document.querySelector('#chart1'); // Select canvas for rendering chart
    chart1 = new Chart(ctx, config1 ); // create chart*/
});

onBeforeUnmount(() => {
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
});

// For the real-time chart
const MAX_CHART_POINTS = 40; // Show last 60 seconds (adjust as needed)
// Expand chartHistory to hold arrays for all plottable metrics
const chartHistory = reactive({
  timestamps: [],
  temperature: [],
  humidity: [],
  pressure: [], // Store raw Pascal values
  heatindex: [],
  moisture: [],
  altitude: []  // Store raw meter values
});

// WATCHERS
watch(payload, (newPayload) => {
  if (newPayload) {
    chartHistory.timestamps.push(newPayload.timestamp);
    chartHistory.temperature.push(newPayload.temperature);
    chartHistory.humidity.push(newPayload.humidity);
    chartHistory.pressure.push(newPayload.pressure);
    chartHistory.heatindex.push(newPayload.heatindex);
    chartHistory.moisture.push(newPayload.moisture);
    chartHistory.altitude.push(newPayload.altitude);
    // fetchData(newPayload); // Fetch data when payload changes
    console.log('MQTT payload received:', newPayload);
    console.log(chartHistory);
  }
});

const chartData = computed(() => {
  const metricKey = selectedChartMetric.value; // e.g., 'temperature', 'humidity'

  // Check if the selected metric's history exists and has data
  if (!chartHistory[metricKey] || chartHistory[metricKey].length === 0) {
    return { labels: [], datasets: [] }; // Return empty structure if no data
  }

  let dataPoints = [];
  let unitLabel = '';
  const sourceData = chartHistory[metricKey]; // Get the raw data array (e.g., chartHistory.temperature)

  // Process data points: Apply unit conversions based on selected metric and units
  dataPoints = sourceData.map(value => {
    if (value === null || value === undefined) return null; // Handle potential nulls in history

    switch (metricKey) {
      case 'temperature':
      case 'heatindex':
        unitLabel = "°C"; // Use pre-calculated unit label (°C or °F)
        return value;
      case 'pressure':
        unitLabel = "hPa"; // Use pre-calculated unit label (hPa or inHg)
        return value;
      case 'altitude':
        unitLabel = "m"; // Use pre-calculated unit label (m or ft)
        return value;
      case 'humidity':
      case 'moisture':
        unitLabel = '%';
        return value; // No conversion needed for percentage values
      default:
        unitLabel = ''; // Should not happen with dropdown
        return value;
    }
  });

  // Capitalize metric name for label (e.g., "Temperature")
  const metricName = metricKey.charAt(0).toUpperCase() + metricKey.slice(1);

  // Define distinct colors for different metrics
  const colors = {
    temperature: '#808000', // Blue
    humidity: '#808000',    // Teal
    pressure: '#808000',    // Orange
    heatindex: '#808000',   // Red
    moisture: '#808000',    // Green
    altitude: '#808000'     // Purple
  };
  const color = colors[metricKey] || '#777777'; // Default grey if key not found

  return {
    labels: chartHistory.timestamps, // Use the timestamps array
    datasets: [
      {
        label: `${metricName} (${unitLabel})`, // Dynamic label
        backgroundColor: color,           // Dynamic color
        borderColor: color,               // Dynamic color
        data: dataPoints,                 // Processed data points
        tension: 0.1,
        pointRadius: 1,
        fill: false,
      },
    ],
  };
});

const chartOptions = computed(() => {
  const metricKey = selectedChartMetric.value;
  let yAxisLabel = metricKey.charAt(0).toUpperCase() + metricKey.slice(1);
  let beginAtZero = false; // Default: don't force y-axis to start at 0

  // Set Y-axis label based on metric and units, decide if starting at zero makes sense
  switch (metricKey) {
    case 'temperature': yAxisLabel += "°C"; break;
    case 'heatindex': yAxisLabel += "°C"; break;
    case 'pressure': yAxisLabel += "hPa"; break;
    case 'altitude': yAxisLabel += "m"; break;
    case 'humidity':
      yAxisLabel += ' (%)';
      beginAtZero = true; // Percentages often start at 0
      break;
    case 'moisture':
      yAxisLabel += ' (%)';
      beginAtZero = true; // Percentages often start at 0
      break;
  }

  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 0 }, // Fast updates for live data
    scales: {
      x: {
        type: 'timeseries',
        time: {
          unit: 'second', // Base unit
          tooltipFormat: 'PPpp', // Detailed tooltip time
          displayFormats: { second: 'HH:mm:ss', minute: 'HH:mm' }
        },
        ticks: { source: 'auto', maxTicksLimit: 10 }, // Auto ticks, limit quantity
        title: { display: true, text: 'Time' }
      },
      y: {
        beginAtZero: beginAtZero, // Dynamic based on metric
        title: { display: true, text: yAxisLabel } // Dynamic Y-axis title
      }
    },
    plugins: {
      legend: { display: true, position: 'top' }, // Show legend now we have dynamic labels
      title: { display: false } // Keep using the H3 for main title
    }
  };
});
</script>


<style scoped>
/** CSS STYLE HERE */
.card {
    margin-bottom: 5;
    max-width: 500;
}

Figure {
    border: 2px solid black;
}

container0.container {
    background-color: surface;
}

.chart-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  /* Increased height slightly to accommodate selector? Adjust as needed */
  min-height: 400px;
  display: flex;
  /* Use flexbox for better control */
  flex-direction: column;
  /* Stack title, selector, chart vertically */
}

.chart-container h3 {
  margin-top: 0;
  margin-bottom: 10px;
  /* Space below title */
  text-align: center;
  color: #333;
}

.chart-metric-selector {
  margin-bottom: 15px;
  /* Space below selector */
  text-align: center;
  /* Center selector elements */
}

.chart-metric-selector label {
  margin-right: 8px;
  font-weight: bold;
  color: #555;
}

.chart-metric-selector select {
  padding: 5px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
}

/* Ensure LineChart component takes remaining space */
.chart-container> :deep(canvas),
/* Target canvas inside LineChart */
.chart-container>p

/* Target "Collecting data..." text */
  {
  flex-grow: 1;
  /* Allow chart/placeholder to fill available space */
  min-height: 250px;
  /* Ensure it doesn't collapse */
}

.chart-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);

  /* *** 1. SET A FIXED HEIGHT *** */
  height: 400px;
  /* Adjust this value as needed */
  /* min-height: 400px; */
  /* Replace min-height with height */

  display: flex;
  flex-direction: column;
  /* position: relative; */
  /* Keep if needed, but maybe not required with fixed height */
}

.chart-container h3,
.chart-container .chart-metric-selector {
  /* *** 2. Prevent title/selector from growing/shrinking vertically *** */
  flex-shrink: 0;
}

/* *** 3. Target the chart element/placeholder to grow *** */
/* This targets the <LineChart> component instance or the <p> tag */
.chart-container> :nth-last-child(1):not(h3):not(.chart-metric-selector) {
  flex-grow: 1;
  /* Allow it to take up remaining space */

  /* *** 4. CRUCIAL: Prevent flex item from expanding container *** */
  min-height: 0;

  /* Add position relative for Chart.js internal calculations if needed*/
  position: relative;
}

h3{
    color: olive;
}

p{
    color: olive;
}

.label{
    color:olive;
}
</style>