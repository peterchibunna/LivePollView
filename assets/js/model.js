const model = document.getElementById("model")
const modelInner = document.getElementById("model-inner")
const closeBtn = document.getElementById("close-btn")
const innerButton = document.getElementById("inner-button")
const modelText = document.getElementById("model-text")
const inForm = document.getElementById("in-form")


setTimeout(function() {
    model.style.display = "inline"
}, 2500)

closeBtn.addEventListener("click", () => model.style.display = "none")

document.getElementById("decline-button").addEventListener("mouseenter", () => innerButton.classList.toggle("inner-button-reverse"))

inForm.addEventListener("submit", function(e) {
    e.preventDefault()

    const inFormData = new FormData(inForm)
    const fullName = inFormData.get("fullName")
    console.log(fullName)

    modelText.innerHTML = `
    <div class = "model-inner-loading">
        <img src = "assets/images/loading.svg" class = "loading"/>
        <p id = "upload-text">We are saving your data in our server. Please hold on for a few seconds...</p>
    </div>
    `
    setTimeout(() =>{
        document.getElementById("upload-text").textContent = "Finishing things up..."
    }, 1500)

    setTimeout(() => {
        modelInner.innerHTML = `
        <h2 class = "inner-thanks">Thank you <span class = "inner-name">${fullName}</span> for your trust!</h2>
        <p>You are now been set up! you can close this box now at the top-right conner!</p>
        <div class = "validate">
            <img src = "assets/images/agree.gif" class = "agree">
        </div>
        `
        closeBtn.disabled = false
    }, 3000)
})