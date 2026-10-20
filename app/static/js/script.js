// Submit buttons
const name = document.getElementById("name");
const price = document.getElementById("price");
const cycle= document.getElementById("cycle");
const category = document.getElementById("category");
const billDate = document.getElementById("billDate");
const urlLink = document.getElementById("urlLink");
const remind = document.getElementById("remind");


// Success modal
const toggleModal = (person, motionEnabled) => {
    let modal = document.getElementById("success-modal");
    let modalContent = document.getElementById("modal-text");
    
    // TODO: Update modal display to flex
    modal.style.display = "flex";

    // TODO: Update modal text to personalized message
    modalContent.textContent = "Eye's up " + person.clas + "!";

    // Set modal timeout to 5 seconds
    setTimeout(() => {
      modal.style.display = "none";
      clearInterval(intervalId);
    }, 5000);
    
    //Close button
    let modalButton = document.getElementById("modal-button");

    modalButton.addEventListener("click", () => {
    modal.style.display = "none";
    clearInterval(intervalId);
})
}