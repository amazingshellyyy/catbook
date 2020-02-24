console.log('hii')
let base_url = "http://127.0.0.1:8000/"
$("body").bind("ajaxSend", function(elm, xhr, s){
  if (s.type == "POST") {
     xhr.setRequestHeader('X-CSRF-Token', getCSRFTokenValue());
  }
});
let token = '{{csrf_token}}'
$profileImgSrc = $('#profileImg').prop('src')
$userId = $('#userId').prop('innerText')
console.log($userId)
$savebtn = $('#save')
$backbtn = $('#back')
console.log($savebtn)
$savebtn.on("click", function(){
  $.ajax({
    method: 'POST',
    url: `http://127.0.0.1:8000/test_img/save_image/`,
    data: {
      image_url: $profileImgSrc
    },
    success: function( response ) {
      console.log('success');
      $savebtn.css('display','none')
      $backbtn.css('display','')
    },
    error: function() {
      alert('There was an error changing the profile image.');
    },
  }) 
})
