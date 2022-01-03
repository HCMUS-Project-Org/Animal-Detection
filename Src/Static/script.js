var img_frame = 'img_frame'

function AnimalDetection(image_b64) {
    console.log('Detect animal')

    eel.animalDetection(image_b64)
}

function setImgFramSize(width, height) {
    console.log('width:', width, '- height:', height)
    
    width = width * 20;
    height = height * 20;
    var max_width = 630; 
    var max_height = 450;
    
    if (width > max_width || height > max_width) {
        var scale = width / max_width;

        console.log('scale:', scale)

        height = height / scale;
        width = width / scale;

        if (height > max_height) {
            scale = height / max_height;
            height = height / scale;
            width = width / scale;
        }
        console.log('adjust width:', width, '- height:', height)

        document.getElementById(img_frame).style.setProperty("height", height.toString() + 'px', 'important')
        document.getElementById(img_frame).style.setProperty("width", width.toString() + 'px', 'important')
    }
}

eel.expose(getResultBase64Image)
function getResultBase64Image(b64_img){
    console.log(b64_img)
    return b64_img
}

function uploadImg(obj) {
    if (FileReader)	{
		var reader = new FileReader();
		reader.readAsDataURL(obj.files[0]);
        console.log('reader:',reader)

        reader.onload = function (e) {

            var img_base64 = reader.result

            var image = new Image();
            image.src=e.target.result;	
            
            image.onload = function () {
                // load origin image
                document.getElementById(img_frame).src=image.src;
                setImgFramSize(this.width, this.height)

                // detect animal
                AnimalDetection(img_base64)
                
                // load detected image 
                document.getElementById(img_frame).src = './picture/result.jpg'
            };
		}
	}
    // ref: https://stackoverflow.com/questions/3814231/loading-an-image-to-a-img-from-input-file
}


function deleteImg() {
    document.getElementById(img_frame).src = './picture/white.png';
    document.getElementById(img_frame).style.setProperty("height", '450px', 'important')
    document.getElementById(img_frame).style.setProperty("width", '100%', 'important')
    console.log("Image deleted");
}

