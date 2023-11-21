const imageContainer = document.querySelector('.scrollable');
const selectedList = document.getElementById('selected-list');

// Sample image data (you can replace this with your own data)
const imageData = [
    { src: 'image1.jpg', description: 'Image 1 Description', mainDetails: 'Main Details 1' },
    { src: 'image2.jpg', description: 'Image 2 Description', mainDetails: 'Main Details 2' },
    // Add more image data as needed
];

// Load images and descriptions dynamically
imageData.forEach((data) => {
    const imgElement = document.createElement('img');
    imgElement.src = data.src;
    imgElement.alt = data.description;
    
    // Add click event to capture main details and add to the selected list
    imgElement.addEventListener('click', () => {
        const listItem = document.createElement('li');
        listItem.textContent = data.mainDetails;
        selectedList.appendChild(listItem);
    });

    const descriptionElement = document.createElement('p');
    descriptionElement.textContent = data.description;

    imageContainer.appendChild(imgElement);
    imageContainer.appendChild(descriptionElement);
});

// Enable horizontal scrolling
imageContainer.addEventListener('wheel', (e) => {
    if (e.deltaY !== 0) {
        e.preventDefault();
        imageContainer.scrollLeft += e.deltaY;
    }
});
