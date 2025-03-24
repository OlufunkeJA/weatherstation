<template>
  <VContainer class="fill-height">  
    
    <VResponsive class="align-center text-center fill-height">
      <VImg height="273" class="mb-1" src="@/assets/start.png" />

      <h1>Olufunke's</h1>
      <h1 class="text-h2 font-weight-bold">Weather Station</h1>
 
      <div class="py-5"/>

      <VRow class="d-flex align-center justify-center">
        <VCol cols="auto">
          <VBtn
            class = "start"
            href="/broadcast"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            target="_blank"
            variant="flat"
          >
            <VIcon icon="mdi-broadcast" size="large" start />
            <!--mdi-temperature celcius -->
            Real-time Weather Updates
          </VBtn>
        </VCol>
      </VRow>
    </VResponsive>
  </VContainer>

</template>

<script setup>
  import { storeToRefs } from 'pinia';
  import { useMqttStore } from '@/store/mqttStore';
  import { ref,reactive, watch, onMounted, onBeforeUnmount } from 'vue';
 

// VARIABLES


// FUNCTIONS
onMounted(()=>{
   
});

onBeforeUnmount(()=>{ 
  
});
</script>

<style>
.start{
  background-color: olive;
  color: white;
}

h1{
  color: olive;
}

</style>