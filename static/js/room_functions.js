let msg_image_clear = document.querySelector(".msg_clear_svg");
let id_message_image = document.querySelector("#id_message_image");
let msg_clear_svg = document.querySelector(".msg_clear_svg")
let msg_send_icon = document.querySelector(".msg_send_icon")

let message_box_input = document.querySelector(".message_box_input");


const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;
const scrollElement = document.querySelector(".room__messages");
function reset_form_element() {
  id_message_image.value = "";
  message_box_input.value = "";
  message_box_input.readOnly = false;
}
msg_image_clear.onclick = () => {
  reset_form_element();
};

document.getElementById("id_message_image").addEventListener("change", () => {
    document.querySelector(".message_box_input").focus();
});
id_message_image.onchange = (e) => {
    if(e.target.value != ""){
      console.log(e.target.value);
      var s = e.target.value;
      var filename = "";
      for(var i = 0; i < s.length; i++){
        filename += s[i];
        if(s[i] == '\\'){
          filename = "";
        }
      }
      message_box_input.value = filename;
      message_box_input.readOnly = true;
    }else{
      reset_form_element();
    }
  }


  



scrollToBottom(scrollElement);
function scrollToBottom(element) {
element.scroll({ top: element.scrollHeight, behavior: 'smooth' });
}



