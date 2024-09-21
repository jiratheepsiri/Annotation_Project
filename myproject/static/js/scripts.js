/*!
* Start Bootstrap - Personal v1.0.1 (https://startbootstrap.com/template-overviews/personal)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-personal/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

//---------------------------------------------------------------------------------------------------------------------------
//for text verify
document.addEventListener('DOMContentLoaded', function() {
    const textForm = document.getElementById('text-form');
    if (textForm) {
        textForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const inputText = document.getElementById('text-input').value.trim();

            if (inputText === "") {
                alert("กรุณากรอกข้อความ");
                return;
            }

            // Display the analysis result (mockup)
            document.getElementById('result').style.display = 'block';
            document.getElementById('analysis-result').innerText = `"${inputText}" เป็นข้อความเชิงบูลลี่ในหมวดใดหมวดหนึ่ง`;
        });
    }
});
//for file verify
document.addEventListener('DOMContentLoaded', function() {
    const fileForm = document.getElementById('file-form');
    if (fileForm) {
        fileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const fileInput = document.getElementById('file-upload');
            const file = fileInput.files[0];

            if (!file) {
                alert("กรุณาอัปโหลดไฟล์");
                return;
            }

            const allowedExtensions = ['csv', 'xml'];
            const fileExtension = file.name.split('.').pop().toLowerCase();

            if (!allowedExtensions.includes(fileExtension)) {
                alert("กรุณาอัปโหลดไฟล์ที่มีนามสกุล .csv หรือ .xml");
                return;
            }

            // Process the file
            alert("กำลังวิเคราะห์ไฟล์: " + file.name);
        });
    }
});
//---------------------------------------------------------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function() {
    const csvButton = document.getElementById('csv-button');
    const xmlButton = document.getElementById('xml-button');
    const csvExample = document.getElementById('csv-example');
    const xmlExample = document.getElementById('xml-example');

    function setActiveButton(activeButton, inactiveButton) {
        // Set active button style
        activeButton.classList.remove('btn-outline-light');
        activeButton.classList.add('btn-light');
        activeButton.classList.add('rounded-pill');
        activeButton.style.color = 'black';

        // Set inactive button style
        inactiveButton.classList.remove('btn-light');
        //inactiveButton.classList.add('btn-outline-light');
        inactiveButton.style.color = 'white';
    }

    // Show CSV example and set CSV button as active by default
    csvExample.style.display = 'block';
    xmlExample.style.display = 'none';
    setActiveButton(csvButton, xmlButton);

    // Event listener for CSV button
    csvButton.addEventListener('click', function() {
        csvExample.style.display = 'block';
        xmlExample.style.display = 'none';
        setActiveButton(csvButton, xmlButton);
    });

    // Event listener for XML button
    xmlButton.addEventListener('click', function() {
        xmlExample.style.display = 'block';
        csvExample.style.display = 'none';
        setActiveButton(xmlButton, csvButton);
    });
});
//for csv and xml file example
// document.addEventListener('DOMContentLoaded', function() {
//     // Get the buttons and example sections
//     const csvButton = document.getElementById('csv-button');
//     const xmlButton = document.getElementById('xml-button');
//     const csvExample = document.getElementById('csv-example');
//     const xmlExample = document.getElementById('xml-example');

//     // Show CSV example by default
//     csvButton.classList.add('btn-primary');
//     xmlButton.classList.add('btn-secondary');

//     // Event listener for CSV button
//     csvButton.addEventListener('click', function() {
//         csvExample.style.display = 'block';  // Show CSV example
//         xmlExample.style.display = 'none';   // Hide XML example

//         // Update button styles
//         csvButton.classList.remove('btn-secondary');
//         csvButton.classList.add('btn-primary');
//         xmlButton.classList.remove('btn-primary');
//         xmlButton.classList.add('btn-secondary');
//     });

//     // Event listener for XML button
//     xmlButton.addEventListener('click', function() {
//         xmlExample.style.display = 'block';  // Show XML example
//         csvExample.style.display = 'none';   // Hide CSV example

//         // Update button styles
//         xmlButton.classList.remove('btn-secondary');
//         xmlButton.classList.add('btn-primary');
//         csvButton.classList.remove('btn-primary');
//         csvButton.classList.add('btn-secondary');
//     });
// });
//---------------------------------------------------------------------------------------------------------------------------
//texttopost
document.getElementById('text-form2').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Get the user's input from the textarea
    const userInput = document.getElementById('text-input2').value;

    // Check if the input is not empty
    if (userInput.trim() !== '') {
        // Simulate sending the input (e.g., send it to a server or log it)
        submitUserInput(userInput);

        // Clear the input field after submission
        document.getElementById('text-input2').value = '';

        // Optionally, show a confirmation or feedback message
        alert('ข้อความคุณถูกส่งเรียบร้อย!');
    } else {
        // If the input is empty, show a warning message
        alert('กรุณากรอกข้อความก่อนส่ง');
    }
});

function submitUserInput(input) {
    // Placeholder for real submission logic, such as an AJAX call to a server
    console.log("Submitted text:", input);

    // You can replace the console.log with a real request to store or process the user's input
}

//texttopostfile

// document.addEventListener('DOMContentLoaded', function() {
//     const fileForm = document.getElementById('file-form2');
//     if (fileForm) {
//         fileForm.addEventListener('submit', function(e) {
//             e.preventDefault();
//             const fileInput = document.getElementById('file-upload2');
//             const file = fileInput.files[0];

//             if (!file) {
//                 alert("กรุณาอัปโหลดไฟล์");
//                 return;
//             }

//             const allowedExtensions = ['csv', 'xml'];
//             const fileExtension = file.name.split('.').pop().toLowerCase();

//             if (!allowedExtensions.includes(fileExtension)) {
//                 alert("กรุณาอัปโหลดไฟล์ที่มีนามสกุล .csv หรือ .xml");
//                 return;
//             }

//             // Process the file
//             alert("กำลังวิเคราะห์ไฟล์: " + file.name);
//         });
//     }
// });

// document.addEventListener('DOMContentLoaded', function() {
//     // Get references to DOM elements
//     const fileForm = document.getElementById('file-form2');
//     const fileInput = document.getElementById('file-upload2');
//     const submitButton = document.getElementById('submit-file-btn');
//     const csvButton = document.getElementById('csv-button');
//     const xmlButton = document.getElementById('xml-button');
//     const csvExample = document.getElementById('csv-example');
//     const xmlExample = document.getElementById('xml-example');

//     // File upload handling
//     fileForm.addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevent the form from submitting normally

//         if (fileInput.files.length === 0) {
//             alert('กรุณาเลือกไฟล์ก่อนกดส่ง'); // Please select a file before submitting
//             return;
//         }

//         const file = fileInput.files[0];
//         const fileName = file.name;
//         const fileExtension = fileName.split('.').pop().toLowerCase();

//         if (fileExtension !== 'csv' && fileExtension !== 'xml') {
//             alert('กรุณาอัปโหลดไฟล์ .csv หรือ .xml เท่านั้น'); // Please upload only .csv or .xml files
//             fileInput.value = ''; // Clear the file input
//             return;
//         }

//         // If we've made it this far, the file is valid
//         alert('ไฟล์ถูกส่งเรียบร้อยแล้ว: ' + fileName); // File submitted successfully: [filename]
//         // Here you would typically send the file to the server
//         // For demonstration, we're just showing an alert
//     });

//     // File input change event for immediate feedback
//     fileInput.addEventListener('change', function() {
//         if (this.files.length > 0) {
//             const file = this.files[0];
//             const fileName = file.name;
//             const fileExtension = fileName.split('.').pop().toLowerCase();

//             if (fileExtension !== 'csv' && fileExtension !== 'xml') {
//                 alert('กรุณาเลือกไฟล์ .csv หรือ .xml เท่านั้น'); // Please select only .csv or .xml files
//                 this.value = ''; // Clear the file input
//             }
//         }
//     });

//     // Toggle between CSV and XML examples
//     csvButton.addEventListener('click', function() {
//         csvExample.style.display = 'block';
//         xmlExample.style.display = 'none';
//         csvButton.classList.add('active');
//         xmlButton.classList.remove('active');
//     });

//     xmlButton.addEventListener('click', function() {
//         xmlExample.style.display = 'block';
//         csvExample.style.display = 'none';
//         xmlButton.classList.add('active');
//         csvButton.classList.remove('active');
//     });

//     // Optional: Toggle between text input and file input
//     const textInputBtn = document.getElementById('text-input-btn');
//     if (textInputBtn) {
//         textInputBtn.addEventListener('click', function() {
//             window.location.href = 'texttopost.html';
//         });
//     }
// });
//------------------------------------------------------------------------