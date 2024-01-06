
import sys
sys.path.append('/tensorfl_vision/tutorial/')
from flask import Flask, render_template, json, jsonify, session, request, flash
from flask import redirect, url_for, send_from_directory
from yolov7_inheritance_batch import *
from flask_cors import CORS
from werkzeug.utils import secure_filename


import os
class yolov7_json_handle:
    
    
    def __init__(self):
        
        self.template_dir = '/tensorfl_vision/tutorial/templates'
        self.static_folder = '/tensorfl_vision/tutorial/static'
        self.app = Flask(__name__, template_folder=self.template_dir, static_folder = self.static_folder)
        
        CORS(self.app)  
        
        self.UPLOAD_FOLDER = '/tensorfl_vision/tutorial/static/uploads/'
        
        # app config
        self.app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER
        self.app.secret_key = 'fikratgasimov'
        
        self.uploaded_file_path = None
        self.last_uploaded_files = []
        self.uploaded_file_path = None 
        
        
        self.ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        
       
        self.path_to_classes = '/tensorfl_vision/Onnx_Yolov4/coco-classes.txt'
        self.image_path = '/tensorfl_vision/Onnx_Yolov4/Images'
        self.path_to_cfg_yolov7 = '/tensorfl_vision/Yolov8/yolov7-tiny.cfg'
        self.path_to_weights_yolov7 = '/tensorfl_vision/Yolov8/yolov7-tiny.weights'
        
        self.flask_path = '/tensorfl_vision/tutorial/static/uploads'
        
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)


        self.app.add_url_rule('/tutorial/home', view_func = self.main_page)
    
        
        self.app.add_url_rule('/tutorial/sign', view_func = self.sign)
        
        self.app.add_url_rule('/tutorial/registration', view_func = self.registration)
    
        self.app.add_url_rule('/tutorial/system-works', view_func = self.system_works)
        
        self.app.add_url_rule('/tutorial/dl-inference', view_func = self.dl_inference)
        
        # RENDER JSON OBJECT DETECTION
        self.app.add_url_rule('/tutorial/process-data', view_func=self.render_postproces, methods=['POST'])
        
        self.app.add_url_rule('/tutorial/dl-image-inference', view_func = self.dl_image_inference, methods = ['POST', 'GET'])
        
        self.app.add_url_rule('/tutorial/last-uploaded', view_func = self.getlastFile, methods=['GET'])
            
        self.app.add_url_rule('/tutorial/about-me', view_func = self.about_me)

    
     # ALLOWED FILE    
    def allowed_file(self, filename):
        
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    
    def main_page(self):
        
        return render_template('main.html')
    
    def sign(self):
        return render_template('sign.html')    

    def registration(self):
        return render_template('registration.html')    
    
    def system_works(self):
        return render_template('system_works.html')
    
    def dl_inference(self):
        return render_template('dl_inference.html')
    
    def about_me(self):
        return render_template('about_me.html')
    
    
    def dl_image_inference(self):
        if request.method == 'POST':
           
            file = request.files['image_name']
            
            if file and self.allowed_file(file.filename):
                
                filename = secure_filename(file.filename)
                # get file name
                self.last_uploaded_files.append(filename)
                
                if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
                    
                    os.makedirs(self.app.config['UPLOAD_FOLDER'])
                    
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                
                file.save(file_path)
               # print('**************',file_path, filename)
                processor_inference = Yolov7Processor(0.3, 0.38, self.path_to_classes, file_path, self.path_to_cfg_yolov7, self.path_to_weights_yolov7,
                                                      single_image=True)
               
                getImagesInference = processor_inference.inference_image_run(file_path)
              
                if getImagesInference:
                    # Convert to relative paths
                    relative_paths = [os.path.relpath(img_path, '/tensorfl_vision/tutorial/static') for img_path in getImagesInference]
                    flash('File successfully uploaded')
                    return render_template('dl_image_inference.html', upload=True, upload_image=relative_paths)
                    
              
        
        return render_template('dl_image_inference.html', upload=False)
    
    
    def getlastFile(self):
        
        print("LAST UPLOAD", self.last_uploaded_files)
        
        return jsonify(self.last_uploaded_files)
        
     
    def render_postproces(self):
        
        try:
            processor = Yolov7Processor(0.3, 0.38, self.path_to_classes, self.image_path, self.path_to_cfg_yolov7, self.path_to_weights_yolov7)
            data = processor.get_results_as_json()
            return jsonify(data)

        except Exception as e:
            print("Error", e)
            return str(e)
        


if __name__ == "__main__":
    yolov7_flask =  yolov7_json_handle()
   
    yolov7_flask.app.run(debug=True)
        
        
        
