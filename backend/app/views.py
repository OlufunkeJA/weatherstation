"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

# from crypt import methods
import site 

from app import app, Config,  mongo, Mqtt
from markupsafe import escape
from flask import render_template, request, jsonify, send_file, redirect, make_response, send_from_directory 
from json import dumps, loads 
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta, timezone
from os import getcwd
from os.path import join, exists
from time import time, ctime
from math import floor
 



#####################################
#   Routing for your application    #
#####################################

@app.route('/api/range/<start>/<end>', methods=['GET']) 
def get_range(start,end):   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            Start = escape(start)
            End = escape(end)
            data = mongo.range(Start,End)

            if data:
                return jsonify({"status":"found","data": data})
            
        except Exception as e:
            print(f"get_range error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})

@app.route('/api/mmar/temperature/<start>/<end>', methods=['GET']) 
def get_temperature_mmar(start,end):   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            Start = escape(start)
            End = escape(end)
            timestampTemp = mongo.temperatureMMAR(Start,End)            

            if timestampTemp:
                return jsonify({"status":"found","data": timestampTemp})
            
        except Exception as e:
            print(f"get_temperature_mmar error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})

@app.route('/api/mmar/humidity/<start>/<end>', methods=['GET']) 
def get_humidity_mmar(start,end):   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            Start = escape(start)
            End = escape(end)
            timestampHumid = mongo.humidityMMAR(Start,End)
            
            if timestampHumid:
                return jsonify({"status":"found","data": timestampHumid})
            
        except Exception as e:
            print(f"get_humidity_mmar error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})


@app.route('/api/mmar/heatIndex/<start>/<end>', methods=['GET']) 
def get_heatIndex_mmar(start,end):   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            Start = escape(start)
            End = escape(end)
            timestampHI = mongo.heatIndexMMAR(Start,End)
            
            if timestampHI:
                return jsonify({"status":"found","data": timestampHI})
            
        except Exception as e:
            print(f"get_heatIndex_mmar error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})


@app.route('/api/mmar/pressure/<start>/<end>', methods=['GET']) 
def get_pressure_mmar(start,end):   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            Start = escape(start)
            End = escape(end)
            timestampPress = mongo.pressureMMAR(Start,End)
            
            if timestampPress:
                return jsonify({"status":"found","data": timestampPress})
            
        except Exception as e:
            print(f"get_pressure_mmar error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})


@app.route('/api/mmar/altitude/<start>/<end>', methods=['GET']) 
def get_altitude_mmar(start,end):   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            Start = escape(start)
            End = escape(end)
            timestampAlt = mongo.altitudeMMAR(Start,End)
            
            if timestampAlt:
                return jsonify({"status":"found","data": timestampAlt})
            
        except Exception as e:
            print(f"get_altitude_mmar error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})


@app.route('/api/mmar/moisture/<start>/<end>', methods=['GET']) 
def get_moisture_mmar(start,end):   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            Start = escape(start)
            End = escape(end)
            timestampMoist = mongo.moistureMMAR(Start,End)
            
            if timestampMoist:
                return jsonify({"status":"found","data": timestampMoist})
            
        except Exception as e:
            print(f"get_moisture_mmar error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})



@app.route('/api/temperature', methods=['GET']) 
def get_temperature():   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            temp = mongo.temperature()

            if temp:
                return jsonify({"status":"found","data": temp})
            
        except Exception as e:
            print(f"get_temperature error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})


@app.route('/api/humidity', methods=['GET']) 
def get_humidity():   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            humid = mongo.humidity()

            if humid:
                return jsonify({"status":"found","data": humid})
            
        except Exception as e:
            print(f"get_humidity error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})

@app.route('/api/heatIndex', methods=['GET']) 
def get_heatIndex():   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            hIndex = mongo.heatIndex()

            if hIndex:
                return jsonify({"status":"found","data": hIndex})
            
        except Exception as e:
            print(f"get_heatIndex error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})

@app.route('/api/pressure', methods=['GET']) 
def get_pressure():   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            pressure = mongo.pressure()

            if pressure:
                return jsonify({"status":"found","data": pressure})
            
        except Exception as e:
            print(f"get_pressure error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})

@app.route('/api/altitude', methods=['GET']) 
def get_altitude():   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            altitude = mongo.altitude()

            if altitude:
                return jsonify({"status":"found","data": altitude})
            
        except Exception as e:
            print(f"get_altitude error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})

@app.route('/api/moisture', methods=['GET']) 
def get_moisture():   
   
    if request.method == "GET": 
        '''Add your code here to complete this route'''
        try:
            moisture = mongo.moisture()

            if moisture:
                return jsonify({"status":"found","data": moisture})
            
        except Exception as e:
            print(f"get_moisture error: f{str(e)}") 

    # FILE DATA NOT EXIST
    return jsonify({"status":"not found","data":[]})

@app.route('/api/file/get/<filename>', methods=['GET']) 
def get_images(filename):   
    '''Returns requested file from uploads folder'''
   
    if request.method == "GET":
        directory   = join( getcwd(), Config.UPLOADS_FOLDER) 
        filePath    = join( getcwd(), Config.UPLOADS_FOLDER, filename) 

        # RETURN FILE IF IT EXISTS IN FOLDER
        if exists(filePath):        
            return send_from_directory(directory, filename)
        
        # FILE DOES NOT EXIST
        return jsonify({"status":"file not found"}), 404


@app.route('/api/file/upload',methods=["POST"])  
def upload():
    '''Saves a file to the uploads folder'''
    
    if request.method == "POST": 
        file     = request.files['file']
        filename = secure_filename(file.filename)
        file.save(join(getcwd(),Config.UPLOADS_FOLDER , filename))
        return jsonify({"status":"File upload successful", "filename":f"{filename}" })

 


###############################################################
# The functions below should be applicable to all Flask apps. #
###############################################################


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(405)
def page_not_found(error):
    """Custom 404 page."""    
    return jsonify({"status": 404}), 404



