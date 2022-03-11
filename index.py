from flask import Flask, jsonify, request, send_file
from flask_restful import Resource, Api
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
api = Api(app)

class CHK(Resource):
    def get(self):
        return jsonify({'message': 'RUNNING'})
    def post(self):
        data = request.get_json()    
        return jsonify({'data': data}), 201
  
  
def imageman(txt):
    THE_TEXT = txt
    with open('Images/wall.jpg', 'rb') as file:
        bgr_img = Image.open(file)
        bgr_img = bgr_img.convert('RGBA')  
        bgr_img_width, bgr_img_height = bgr_img.size
        cx, cy = bgr_img_width//2, bgr_img_height//2

    fgr_img = Image.new('RGBA', bgr_img.size, color=(0, 0, 0, 0))

    font_size = bgr_img_width//len(THE_TEXT)
    font = ImageFont.truetype('Fonts/Spider-Man.otf', font_size)

    txt_width, txt_height = font.getsize(THE_TEXT)  
    tx, ty = cx - txt_width//2, cy - txt_height//2  

    mask_img = Image.new('L', bgr_img.size, color=255)
    mask_img_draw = ImageDraw.Draw(mask_img)
    mask_img_draw.text((tx, ty), THE_TEXT, fill=0, font=font, align='center')

    res_img = Image.composite(fgr_img, bgr_img, mask_img)
    res_img.save('LOG/resdownload.png')
    return send_file('LOG/resdownload.png', as_attachment=True)

class Manipulator(Resource):
    def get(self, txt):
        imageman(txt)
        return 0
  

api.add_resource(CHK, '/')
api.add_resource(Manipulator, '/man/<string:txt>')
  

if __name__ == '__main__':
    app.run(debug = True)
