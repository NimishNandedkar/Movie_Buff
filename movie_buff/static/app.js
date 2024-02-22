//Below code is for slider 
var nextButtons = document.querySelectorAll('.next-button');
var prevButtons = document.querySelectorAll('.prev-button');
var movieLists = document.querySelectorAll(".movie-list");

nextButtons.forEach((nextButton, i) => {
    nextButton.addEventListener("click", () => {
        console.log("Next button clicked");
        const itemNumber = movieLists[i].querySelectorAll("img").length;
        const slideWidth = 270; // Width of each slide
        const sliderWidth = window.innerWidth; // Width of the slider container
        const slidesVisible = Math.floor(sliderWidth / slideWidth); // Calculate number of visible slides
        const maxSlides = itemNumber - slidesVisible; // Maximum number of slides before reaching the end

        let clickCounter = parseInt(movieLists[i].getAttribute('data-counter')) || 0;
        clickCounter++;
        
        if (clickCounter <= maxSlides) {
            clickCounter++;
        }
        // code to return the slider to its oringnal posttion
        else{                                                               
            clickCounter=0;
        }
            movieLists[i].style.transform = `translateX(-${clickCounter * slideWidth}px)`;
            movieLists[i].setAttribute('data-counter', clickCounter.toString());
        
    });
});

prevButtons.forEach((prevButton, i) => {
    prevButton.addEventListener("click", () => {
        console.log("prev button clicked");
        const slideWidth = 270; // Width of each slide
        
        let clickCounter = parseInt(movieLists[i].getAttribute('data-counter')) || 0;
        
        if (clickCounter > 0) {
            clickCounter--;
            movieLists[i].style.transform = `translateX(-${clickCounter * slideWidth}px)`;
            movieLists[i].setAttribute('data-counter', clickCounter.toString());
        }
    });
});





