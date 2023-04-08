const model = document.getElementById("model")
const closeBtn = document.getElementById("close-btn")
const innerButton = document.getElementById("inner-button")
const modelText = document.getElementById("model-inner")
const inForm = document.getElementById("in-form")


setTimeout(function() {
    model.style.display = "inline"
}, 2500)
closeBtn.addEventListener("click", () => model.style.display = "none")

document.getElementById("decline-button").addEventListener("mouseenter", () => innerButton.classList.toggle("inner-button-reverse"))

inForm.addEventListener("submit", function(e) {
    e.preventDefault()

    modelText.innerHTML = `
    <h2>We are here to try out something magical</h2>
    `
})