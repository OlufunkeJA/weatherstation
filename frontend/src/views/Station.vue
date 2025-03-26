<template>
    <VResponsive class = "screen">
    <!---->

    <VRow align = "center">
        <VCol align = "center">
            <v-card density="compact" border flat rounded="md" class = "card" color = "primary" variant = "tonal">
                <v-card-item>
                    
                    <strong><p><VIcon icon="mdi-sun-thermometer" size="x-small" start/>Temperature</p></strong>
                    <span class = "span">{{ temperature }}
                        <!--<VIcon icon="mdi-temperature-celsius" size="x-small" />-->
                    </span>
                </v-card-item>
            </v-card>
        </VCol>

        <VCol align = "center">
            <v-card density="compact" border flat rounded="md" class = "card" color = "primary" variant = "tonal">
                <v-card-item>
                    <strong><p><VIcon icon="mdi-water-percent" size="x-small" start/>Humidity</p></strong>
                    <span class = "span">{{ humidity }}</span>
                </v-card-item>
            </v-card>
        </VCol>

        <VCol align = "center">
            <v-card density="compact" border flat rounded="md" class = "card" color = "primary" variant = "tonal">
                <v-card-item>
                    <strong><p><VIcon icon="mdi-thermometer" size="x-small" start/>Heat Index</p></strong>
                    <span class = "span span">{{ heatIndex }}
                        <!--<VIcon icon="mdi-temperature-celsius" size="x-small" start/>-->
                    </span>
                </v-card-item>
            </v-card>
        </VCol>
    </VRow>

    <VRow align = "center">
        <VCol align = "center">
            <v-card density="compact" border flat rounded="md" class = "card" color = "primary" variant = "tonal">
                <v-card-item>
                    <!--Altitude-->
                    <strong><p><VIcon icon="mdi-image-filter-hdr" size="x-small" start/>Altitude</p></strong>
                        <span class = "span span">{{ altitude }}
                        </span>
                </v-card-item>
            </v-card>
        </VCol>

        <VCol align = "center">
            <v-card density="compact" border flat rounded="md" class = "card1" color = "primary" variant = "tonal">
                <v-card-item>
                    <!--Pressure-->
                    <strong><p><VIcon icon="mdi-waves-arrow-up" size="x-small" start/>Pressure</p></strong>
                    <span class = "span1">{{ pressure }}</span>
                </v-card-item>
            </v-card>
        </VCol>

        <VCol align = "center">
            <v-card density="compact" border flat rounded="md" class = "card" color = "primary" variant = "tonal">
                <v-card-item>
                    <!--Soil Moisture-->
                    <strong><p><VIcon icon="mdi-water-opacity" size="x-small" start/>Moisture</p></strong>
                    <span class = "span">{{ moisture }}</span>
                </v-card-item>
            </v-card>
        </VCol>
    </VRow>

    <VRow align = "center">
        <VCol align = "center">
            <VBtn @click="changeUnit()" class = "text-caption" text = "CHANGE TEMP & HEAT INDEX UNITS" variant = "tonal"></VBtn>
        </VCol>
    </VRow>
    <!--<VRow align = "center" class = "bottom">
        <VCol align = "center">
            <VBtn class = "btn" variant = "plain" size = "x-small" justify = "center" v-if="!connectMqtt == true" @click = "buttonClick(this)" >
                <v-icon size="10" icon="mdi-alert-circle-check"></v-icon>     
                MQTT Connected!        
            </VBtn>
            <VBtn class = "btn" variant = "plain" size = "x-small" justify = "center" v-if="!connectMqtt == false">
                <v-icon size="10" icon="mdi-alert-circle"></v-icon>             
                MQTT Not Connected!
            </VBtn>
        </VCol>
    </VRow>-->
    
    <VImg src="@/assets/grass.png" />
    </VResponsive>
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
const Mqtt = useMqttStore();
const { payload, payloadTopic,connectMqtt } = storeToRefs(Mqtt);  
let temp = "C";

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

const temperature = computed(()=>{
if(!!payload.value){
    if (temp == "C"){
        return `${payload.value.temperature.toFixed(2)} °C`;
    }
    if (temp == "F"){
        return `${((payload.value.temperature*9/5)+32).toFixed(2)} F`;
    }
}
});

const heatIndex = computed(()=>{
if(!!payload.value){
    if (temp == "C"){
        return `${payload.value.heatindex.toFixed(2)} °C`;
    }
    if (temp == "F"){
        return `${((payload.value.heatindex*9/5)+32).toFixed(2)} F`;
    }
}
});

const humidity = computed(()=>{
if(!!payload.value){
return `${payload.value.humidity.toFixed(2)} %`;
}
});

const altitude = computed(()=>{
if(!!payload.value){
return `${payload.value.altitude.toFixed(2)} m`;
}
});

const pressure = computed(()=>{
if(!!payload.value){
return `${payload.value.pressure.toFixed(2)} hPa`;
}
});

const moisture = computed(()=>{
if(!!payload.value){
return `${payload.value.moisture.toFixed(2)} %`;
}
});

const changeUnit = async () => {
    if(temp == "C"){
        temp = "F";
    }
    else if (temp == "F"){
        temp = "C";
    }
}
</script>


<style scoped>
/** CSS STYLE HERE */

.card{
    width: 400px;
    height:200px;
    padding: 20px;
}

.card1{
    padding:30px;
    width: 400px;
    height:200px;
}

.text-caption{
    background-color: olive;
    color: white;
}

.span{
    text-emphasis-color: olive;
}

.text-primary{
    text-size-adjust: 50;
}

p{
    font-size: 24px;
}

span{
    font-size:75px;
}

.span1{
    font-size:60px;
}
</style>
  