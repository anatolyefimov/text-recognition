const $fileiInput = document.querySelector('.file')
const $image = document.querySelector('.image')
const $text = document.querySelector('.text')

$fileiInput.addEventListener('change', function(event) {
    const formData = new FormData();
    
    formData.append('file', event.target.files[0])
    var myHeaders = new Headers();
    myHeaders.append('pragma', 'no-cache');
    myHeaders.append('cache-control', 'no-cache');


    fetch('http://localhost:5000/', {
        method: 'POST',
        // headers: {
        //     'Content-Type':'multipart/form-data'
        // },
        body: formData
    })  
        .then(res => res.json())
        .then(res => {
            $text.innerHTML = res.recognizedText;
            return fetch('http://localhost:5000/get_res?v=1', {
                method: 'GET',
                headers: myHeaders
            })
        })  
        .then(res => res.blob())
        .then (blob => $image.src = URL.createObjectURL(blob))
        // .then(blob => { $image.src = URL.createObjectURL(blob)}) 
    
        

})