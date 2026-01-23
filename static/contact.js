const chatButton = document.getElementById("chatButton");
const chatPopup = document.getElementById("chatPopup");
const closeChat = document.getElementById("closeChat");
const chatBox = document.getElementById("chatBox");
const chatButtons = document.getElementById("chatButtons");
const userInput = document.getElementById("userMessage");

// Safe localStorage load
let chatMemory = [];
try {
    chatMemory = JSON.parse(localStorage.getItem("chatMemory")) || [];
} catch(e){ chatMemory = []; }

// Support categories
const supportData = {
    "Order":["Track Order","Cancel Order","Order Not Received","Order Delayed","Change Address","Invoice Download"],
    "Payment":["Payment Failed","Refund Status","Charged Twice","Refund Delay","Payment Method Change","EMI Issue"],
    "Delivery":["Late Delivery","Delivery Reschedule","Wrong Item","Damaged Product","Missing Item","Delivery Partner Issue"],
    "Account":["Login Issue","OTP Not Received","Change Password","Update Email","Update Phone","Deactivate Account"],
    "Other":["Return Item","Replacement","Warranty","Feedback","Complaint","Contact Support"]
};

// Floating chat toggle
chatButton.addEventListener("click", ()=>{
    chatPopup.style.display="flex";
    renderMemory();
    if(chatMemory.length===0){
        bot("👋 Thank you for contacting us. Our support team will assist you shortly.", true);
        setTimeout(()=>bot("💬 How can I help you? Type 'menu' to see options.", true),700);
        setTimeout(()=>showCategories(),1200);
    }
});

// Close chat
closeChat.addEventListener("click", ()=>{ chatPopup.style.display="none"; });

// Clear chat
function clearChat(){
    localStorage.removeItem("chatMemory");
    chatMemory=[];
    chatBox.innerHTML="";
    showCategories();
}

// Render previous messages
function renderMemory(){
    chatBox.innerHTML="";
    chatMemory.forEach(m=>{
        addMessage(m.type,m.text,false);
    });
    showCategories();
}

// Show main categories
function showCategories(){
    chatButtons.innerHTML="";
    Object.keys(supportData).forEach(cat=>{
        const btn=document.createElement("button");
        btn.textContent=cat;
        btn.onclick=()=>showOptions(cat);
        chatButtons.appendChild(btn);
    });
}

// Show sub-options
function showOptions(category){
    addMessage("user-msg",category);
    chatButtons.innerHTML="";
    supportData[category].forEach(opt=>{
        const btn=document.createElement("button");
        btn.textContent=opt;
        btn.onclick=()=>handleOption(opt);
        chatButtons.appendChild(btn);
    });
    bot(`💬 Please select your ${category.toLowerCase()} issue:`, true);
}

// Handle sub-option
function handleOption(option){
    addMessage("user-msg",option);
    chatButtons.innerHTML="";
    bot(getResponse(option), true);
    setTimeout(()=>showCategories(),800);
}

// Responses
function getResponse(option){
    const map = {
        "track order":"📍 Track orders from Order History using Order ID.",
        "cancel order":"❌ Orders can be cancelled before shipment.",
        "order not received":"🚫 If order not received after ETA, we’ll escalate.",
        "order delayed":"⏳ Delays may occur due to logistics issues.",
        "change address":"🏠 Address can be changed before dispatch.",
        "invoice download":"📄 Invoice available in Order Details.",
        "payment failed":"💳 Failed payments auto-refund within 3–5 days.",
        "refund status":"💰 Refunds are processed within 5–7 business days.",
        "charged twice":"⚠️ Extra charges will be refunded automatically.",
        "refund delay":"⏳ Refund delays may occur due to bank processing.",
        "payment method change":"🔄 You can change payment method during checkout.",
        "emi issue":"🏦 EMI issues should be reported to bank support.",
        "late delivery":"🚚 Delivery usually takes 3–7 business days.",
        "delivery reschedule":"📆 Delivery can be rescheduled via order page.",
        "wrong item":"🔄 Wrong item? Request replacement.",
        "damaged product":"📦 Damaged items are eligible for replacement.",
        "missing item":"📭 Missing items will be refunded.",
        "delivery partner issue":"📞 Partner issues are escalated immediately.",
        "login issue":"🔐 Check credentials or reset password.",
        "otp not received":"📲 OTP may take 30 seconds to arrive.",
        "change password":"🔑 Password can be updated from profile.",
        "update email":"📧 Email updates require OTP verification.",
        "update phone":"📱 Phone number can be updated in profile.",
        "deactivate account":"⚠️ Account deactivation is permanent.",
        "return item":"↩️ Returns accepted within 7 days.",
        "replacement":"🔁 Replacement requests processed in 48 hours.",
        "warranty":"🛡️ Warranty details available on product page.",
        "feedback":"📝 We appreciate your feedback!",
        "complaint":"📢 Complaints are handled within 24 hours.",
        "contact support":"📞 Phone: +91 98765 43210\n📧 Email: support@naturecraft.com\n🕘 Mon–Sat 9AM–6PM"
    };
    return map[option.toLowerCase()] || "❓ Sorry, I didn't understand. Please select an option from the menu.";
}

// Typed messages
function sendMessage(){
    const msg=userInput.value.trim();
    if(!msg) return;
    addMessage("user-msg",msg);
    userInput.value="";
    setTimeout(()=>handleTextMessage(msg.toLowerCase()),500);
}

// Handle greetings and menu
function handleTextMessage(msg){
    const greetings=["hi","hello","hey","good morning","good afternoon","good evening"];
    if(greetings.some(g=>msg.includes(g))){
        bot("👋 Thank you for contacting us. Our support team will assist you shortly.", true);
        setTimeout(()=>bot("💬 How can I help you? Type 'menu' to see options.", true),700);
        setTimeout(()=>showCategories(),1200);
        return;
    }
    if(msg==="menu"||msg==="help"){ showCategories(); return; }
    bot("❓ I didn't understand that. Please select a category or click a button.", true);
}

// Add message
function addMessage(cls,text,save=true){
    const div=document.createElement("div");
    div.className=cls;
    div.textContent=text;
    chatBox.appendChild(div);
    chatBox.scrollTop=chatBox.scrollHeight;
    if(save){
        chatMemory.push({type:cls,text});
        localStorage.setItem("chatMemory",JSON.stringify(chatMemory));
    }
}

// Bot typing animation
function bot(text,typing=false){
    if(!typing){ addMessage("bot-msg",text); return; }

    const typingDiv=document.createElement("div");
    typingDiv.className="bot-msg";

    const dots=document.createElement("span");
    dots.className="typing-dots";
    dots.innerHTML="<span></span><span></span><span></span>";

    typingDiv.textContent="💬 ";
    typingDiv.appendChild(dots);
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop=chatBox.scrollHeight;

    setTimeout(()=>{
        typingDiv.textContent=text;
        chatBox.scrollTop=chatBox.scrollHeight;
        chatMemory.push({type:"bot-msg",text});
        localStorage.setItem("chatMemory",JSON.stringify(chatMemory));
    },1000);
}
