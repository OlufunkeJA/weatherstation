<template>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sofia">

    <v-container fluid>
        <!--<VRow align = "center">
            <VCol align = "center">
                <h1>Backcast Analysis</h1>
            </VCol>
        </VRow>-->

        <VRow class = "row" align = "center">
            <VCol>
                <VRow align = "center">
                    <div class="headerDiv">
                        <h1>Backcast</h1>

                        <div class = "py-1" />

                        <div class = "paraDiv">
                            <p>Enter start and end dates to see the max, min, average, and range for that period!</p>
                        </div>
                    </div>                    
                </VRow>
            </VCol>

            <VCol align = "center">
                <v-sheet class = "sheet">
                    <v-text-field class = "textField, textField1" label = "Start Date" type = "Date" density = "compact" variant = "solo-inverted" flat v-model="start"></v-text-field>                
                    <v-text-field class = "textField,textField1" label = "End Date" type = "Date" density = "compact" variant = "solo-inverted" flat v-model="end"></v-text-field>
                </v-sheet>

                <div class = "py-3"/>
                <VBtn @click="updateCards();" class = "text-caption" text = "Analyse"  variant = "plain"></VBtn>
            </VCol>

            <VCol>
                <VImg class="mb-1" src="@/assets/clouds+sun.png" />
            </VCol>
            
        </VRow>

        <VRow align = "center">
            <VCol align = "center">
                <v-card title = "Temperature" width = "auto" variant = "outlined" color = "primary" density = "compact" rounded = "lg" align = "center">
                    <v-card-item width = "auto" class = "mb-n5" align = "center">
                        <v-chip-group width = "auto" class = "d-flex-flex-row justify-center" color = "primaryContainer" variant = "flat" align = "center">
                            <v-tooltip text = "Min" location = "start"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ temperature.min }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Range" location = "top"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ temperature.range }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Max" location = "end"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ temperature.max }}</v-chip></template></v-tooltip>
                        </v-chip-group>
                    </v-card-item>

                    <v-card-item align = "center">
                        <span class = "text-h1 text-primary font-weight-bold">{{ temperature.avg }}</span>
                    </v-card-item>
                </v-card>
            </VCol>

            <VCol  align = "center">
                <v-card title = "Humidity" width = "auto" variant = "outlined" color = "primary" density = "compact" rounded = "lg" align = "center">
                    <v-card-item class = "mb-n5" align = "center">
                        <v-chip-group class = "d-flex-flex-row justify-center" color = "primaryContainer" variant = "flat" align = "center">
                            <v-tooltip text = "Min" location = "start"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ humidity.min }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Range" location = "top"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ humidity.range }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Max" location = "end"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ humidity.max }}</v-chip></template></v-tooltip>
                        </v-chip-group>
                    </v-card-item>

                    <v-card-item align = "center">
                        <span class = "text-h1 text-primary font-weight-bold">{{ humidity.avg }}</span>
                    </v-card-item>
                </v-card>
            </VCol>
            
            <VCol align = "center">
                <v-card title = "Heat Index" width = "auto" variant = "outlined" color = "primary" density = "compact" rounded = "lg">
                    <v-card-item class = "mb-n5" align = "center">
                        <v-chip-group class = "d-flex-flex-row justify-center" color = "primaryContainer" variant = "flat">
                            <v-tooltip text = "Min" location = "start"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ heatIndex.min }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Range" location = "top"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ heatIndex.range }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Max" location = "end"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ heatIndex.max }}</v-chip></template></v-tooltip>
                        </v-chip-group>
                    </v-card-item>

                    <v-card-item align = "center">
                        <span class = "text-h1 text-primary font-weight-bold">{{ heatIndex.avg }}</span>
                    </v-card-item>
                </v-card>
            </VCol>
        </VRow>

        <VRow align = "center">
            <VCol align = "center">
                <v-card title = "Pressure" width = "auto" variant = "outlined" color = "primary" density = "compact" rounded = "lg" align = "center">
                    <v-card-item class = "mb-n5" align = "center">
                        <v-chip-group class = "d-flex-flex-row justify-center" color = "primaryContainer" variant = "flat">
                            <v-tooltip text = "Min" location = "start"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ pressure.min }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Range" location = "top"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ pressure.range }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Max" location = "end"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ pressure.max }}</v-chip></template></v-tooltip>
                        </v-chip-group>
                    </v-card-item>

                    <v-card-item align = "center">
                        <span class = "text-h1 text-primary font-weight-bold">{{ pressure.avg }}</span>
                    </v-card-item>
                </v-card>
            </VCol>

            <VCol  align = "center">
                <v-card title = "Altitude" width = "auto" variant = "outlined" color = "primary" density = "compact" rounded = "lg">
                    <v-card-item class = "mb-n5" align = "center">
                        <v-chip-group class = "d-flex-flex-row justify-center" color = "primaryContainer" variant = "flat">
                            <v-tooltip text = "Min" location = "start"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ altitude.min }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Range" location = "top"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ altitude.range }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Max" location = "end"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ altitude.max }}</v-chip></template></v-tooltip>
                        </v-chip-group>
                    </v-card-item>

                    <v-card-item align = "center">
                        <span class = "text-h1 text-primary font-weight-bold">{{ altitude.avg }}</span>
                    </v-card-item>
                </v-card>
            </VCol>
            
            <VCol align = "center">
                <v-card title = "Moisture" width = "auto" variant = "outlined" color = "primary" density = "compact" rounded = "lg">
                    <v-card-item class = "mb-n5" align = "center">
                        <v-chip-group class = "d-flex-flex-row justify-center" color = "primaryContainer" variant = "flat" justify = "center">
                            <v-tooltip text = "Min" location = "start"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ moisture.min }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Range" location = "top"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ moisture.range }}</v-chip></template></v-tooltip>
                            <v-tooltip text = "Max" location = "end"><template v-slot:activator="{ on, attrs }"><v-chip v-bind="attrs" v-on="on">{{ moisture.max }}</v-chip></template></v-tooltip>
                        </v-chip-group>
                    </v-card-item>

                    <v-card-item align = "center">
                        <span class = "text-h1 text-primary font-weight-bold">{{ moisture.avg }}</span>
                    </v-card-item>
                </v-card>
            </VCol>
        </VRow>
    </v-container>
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS
import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
import { useRoute ,useRouter } from "vue-router";
import { useMqttStore } from '@/store/mqttStore'; // Import Mqtt Store
import { useAppStore } from "@/store/appStore"; 
import {storeToRefs} from "pinia";
 
 
// VARIABLES
const router = useRouter();
const route = useRoute();  
const AppStore = useAppStore();
const start = ref("");
const end = ref("");
const temperature = reactive({"min":0,"max":0,"avg":0,"range":0});
const humidity = reactive({"min":0,"max":0,"avg":0,"range":0});
const heatIndex = reactive({"min":0,"max":0,"avg":0,"range":0});
const pressure = reactive({"min":0,"max":0,"avg":0,"range":0});
const altitude = reactive({"min":0,"max":0,"avg":0,"range":0});
const moisture = reactive({"min":0,"max":0,"avg":0,"range":0});

const Mqtt = useMqttStore();
const { payload, payloadTopic } = storeToRefs(Mqtt);  


// FUNCTIONS
onMounted(()=>{
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    Mqtt.connect(); // Connect to Broker located on the backend
    setTimeout( ()=>{
        // Subscribe to each topic
        Mqtt.subscribe("620162688");
        //Mqtt.subscribe("topic2");
    },3000);
});

onBeforeUnmount(()=>{
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    Mqtt.unsubcribeAll();
});

const updateCards = async () => {
    // Retrieve Min, Max, Avg, Spread/Range
    if(!!start.value && !!end.value){
        //Convert start and end dates collected from TextFields to 10 digit timestamps
        let startDate = new Date(start.value).getTime() / 1000;
        let endDate = new Date(end.value).getTime() / 1000;

        //Fetch data from backend by calling the API functions
        const temp = await AppStore.getTemperatureMMAR(startDate,endDate);
        const humid = await AppStore.getHumidityMMAR(startDate,endDate);
        const heatindex = await AppStore.getHeatIndexMMAR(startDate,endDate);
        const press = await AppStore.getPressureMMAR(startDate,endDate);
        const alt = await AppStore.getAltitudeMMAR(startDate,endDate);
        const moist = await AppStore.getMoistureMMAR(startDate,endDate);
        
        //Temperature MMAR
        temperature.max = temp[0].max.toFixed(1);
        temperature.min = temp[0].min.toFixed(1);
        temperature.avg = temp[0].avg.toFixed(1);
        temperature.range = temp[0].range.toFixed(1);

        //Humidity MMAR
        humidity.max = humid[0].max.toFixed(1);
        humidity.min = humid[0].min.toFixed(1);
        humidity.avg = humid[0].avg.toFixed(1);
        humidity.range = humid[0].range.toFixed(1);

        //Heat Index MMAR
        heatIndex.min = heatindex[0].max.toFixed(1);
        heatIndex.max = heatindex[0].min.toFixed(1);
        heatIndex.avg = heatindex[0].avg.toFixed(1);
        heatIndex.range = heatindex[0].range.toFixed(1);

        //Pressure MMAR
        pressure.min = press[0].max.toFixed(1);
        pressure.max = press[0].min.toFixed(1);
        pressure.avg = press[0].avg.toFixed(1);
        pressure.range = press[0].range.toFixed(1);

        //Altitude MMAR
        altitude.min = alt[0].max.toFixed(1);
        altitude.max = alt[0].min.toFixed(1);
        altitude.avg = alt[0].avg.toFixed(1);
        altitude.range = alt[0].range.toFixed(1);

        //Moisture MMAR
        moisture.min = moist[0].max.toFixed(1);
        moisture.max = moist[0].min.toFixed(1);
        moisture.avg = moist[0].avg.toFixed(1);
        moisture.range = moist[0].range.toFixed(1);
        }
}
</script>

<style scoped>
/** CSS STYLE HERE */
.row{
}

.sheet{
    padding: 2;
    height: 100px;
    width: 200px;
}

.textField{
    max-width: 100px;
}

.textField1{
    margin-right: 5;
}

.text-caption{
    color: olive;
    border-color: olive;
    border-width:2px;
}

h1{
    color: olive;
    font-size:50px;
    font-family: "Sofia", sans-serif;
    text-shadow: 3px 3px 3px #ababab;
}

p{
    color:olive;
    font-size: 16   px;
}

.headerDiv{
    padding: 70px;
    padding-bottom:0px;
    padding-top: 30px;
}

.paraDiv{
    padding: 20px;
    padding-top:0px;
}

.justify-center{
    justify-content: center;
}
</style>
  