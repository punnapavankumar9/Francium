// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}



// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
    photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
        photoPreview.src = URL.createObjectURL(file);
    }
};

document.getElementById("id_message_image").addEventListener("change", () => {
    document.querySelector(".message_box_input").focus();
});

let msg_image_clear = document.querySelector(".msg_clear_svg");
let id_message_image = document.querySelector("#id_message_image");
let msg_clear_svg = document.querySelector(".msg_clear_svg")
let msg_send_icon = document.querySelector(".msg_send_icon")

let message_box_input = document.querySelector(".message_box_input");
function reset_form_element() {
  id_message_image.value = "";
  message_box_input.value = "";
  message_box_input.readOnly = false;
}

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



msg_image_clear.onclick = reset_form_element;


// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

const scrollElement = document.querySelector(".room__messages");
scrollToBottom(scrollElement);

function scrollToBottom(element) {
  element.scroll({ top: element.scrollHeight, behavior: 'smooth' });
}
// let st = document.getElementById("msg_settings");