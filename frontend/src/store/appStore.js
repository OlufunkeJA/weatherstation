import {defineStore} from 'pinia'
import {ref} from 'vue'


export const useAppStore =  defineStore('app', ()=>{

    /*  
    The composition API way of defining a Pinia store
    ref() s become state properties
    computed() s become getters
    function() s become actions  
    */ 

    // STATES 
  


    // ACTIONS
    /*const getTemperature = async () => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `/api/temperature`;

        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });

            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        // console.log(data["data"] )
                    return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("getTemperature returned no data");
                    }
                }
            }
            else{
                const data = await response.text();
                console.log(data);
            }
        }
        catch(err){
            console.error('getTemperature error: ', err.message);
        }
        return []
        }
    

    const getHumidity = async () => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `/api/humidity`;

        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });

            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        // console.log(data["data"] )
                    return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("getHumidity returned no data");
                    }
                }
            }
            else{
                const data = await response.text();
                console.log(data);
            }
        }
        catch(err){
            console.error('getHumidity error: ', err.message);
        }
        return []
        }*/
		
    const getTemperatureMMAR = async (start,end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `http://localhost:5000/api/mmar/temperature/${start}/${end}`;

        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });
            console.log(response);
            console.log(URL);

            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        //console.log(data["data"] )
                    return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("getTemperatureMMAR returned no data");
                    }
                }
            }
            else{
                const data = await response.text(); 
                console.log(data);
            }
        }
        catch(err){
            console.error('getTemperatureMMAR error: ', err.message);
        }
        return []
        }
    
    const getHumidityMMAR = async (start,end) => {
            const controller = new AbortController();
            const signal = controller.signal;
            const id = setTimeout(()=>{controller.abort()},60000);
            const URL = `http://localhost:5000/api/mmar/humidity/${start}/${end}`;
    
            try {
                const response = await fetch(URL,{ method: 'GET', signal: signal });
    
                if (response.ok){
                    const data = await response.json();
                    let keys = Object.keys(data);
                    if(keys.includes("status")){
                        if(data["status"] == "found" ){
                            // console.log(data["data"] )
                        return data["data"];
                        }
                        if(data["status"] == "failed" ){
                            console.log("getHumidityMMAR returned no data");
                        }
                    }
                }
                else{
                    const data = await response.text();
                    console.log(data);
                }
            }
            catch(err){
                console.error('getHumidityMMAR error: ', err.message);
            }
            return []
        }

    const getHeatIndexMMAR = async (start,end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `http://localhost:5000/api/mmar/heatIndex/${start}/${end}`;

        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });
            console.log(response);

            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        // console.log(data["data"] )
                    return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("getHeatIndexMMAR returned no data");
                    }
                }
            }
            else{
                const data = await response.text();
                console.log(data);
            }
        }
        catch(err){
            console.error('getHeatIndexMMAR error: ', err.message);
        }
        return []
        }

    const getPressureMMAR = async (start,end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `http://localhost:5000/api/mmar/pressure/${start}/${end}`;

        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });

            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        // console.log(data["data"] )
                    return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("getPressureMMAR returned no data");
                    }
                }
            }
            else{
                const data = await response.text();
                console.log(data);
            }
        }
        catch(err){
            console.error('getPressureMMAR error: ', err.message);
        }
        return []
        }

    const getAltitudeMMAR = async (start,end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `http://localhost:5000/api/mmar/altitude/${start}/${end}`;

        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });

            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        // console.log(data["data"] )
                    return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("getAltitudeMMAR returned no data");
                    }
                }
            }
            else{
                const data = await response.text();
                console.log(data);
            }
        }
        catch(err){
            console.error('getAltitudeMMAR error: ', err.message);
        }
        return []
        }

    const getMoistureMMAR = async (start,end) => {
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `http://localhost:5000/api/mmar/moisture/${start}/${end}`;

        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });

            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        // console.log(data["data"] )
                    return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("getMoistureMMAR returned no data");
                    }
                }
            }
            else{
                const data = await response.text();
                console.log(data);
            }
        }
        catch(err){
            console.error('getMoistureMMAR error: ', err.message);
        }
        return []
        }

    return { 
        // EXPORTS	
        getHumidityMMAR,
        getTemperatureMMAR,
        getHeatIndexMMAR,
        getPressureMMAR,
        getAltitudeMMAR,
        getMoistureMMAR,
    }
},{ persist: true  });

