import React, { useState } from 'react';
import Webcam from 'react-webcam';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import ClipboardCopy from './CopyText';
import axios from 'axios'; // Import Axios
import Wrapper from '../assets/wrappers/Dashboard';

const WebcamComponent = () => <Webcam />;
const videoConstraints = {
  width: 400,
  height: 400,
  facingMode: 'user',
};

const Stats = () => {
  const [picture, setPicture] = useState('');
  const webcamRef = React.useRef(null);

  const capture = React.useCallback(() => {
    const pictureSrc = webcamRef.current.getScreenshot();
    setPicture(pictureSrc);
    console.log(pictureSrc);
  }, []);

  const sendImageToServer = () => {
    if (picture) {
      // Define the API endpoint where you want to send the image
      const apiUrl = 'https://your-server-api-url.com/upload-image'; // Replace with your server's API URL

      // Create a FormData object to send the image data as a file
      const formData = new FormData();
      formData.append('image', picture);

      // Make the Axios POST request to send the image data
      axios
        .post(apiUrl, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          // Handle the response from the server, e.g., show a success message
          console.log('Image uploaded successfully!', response.data);
          
        })
        .catch((error) => {
          // Handle any errors that occur during the request
          console.error('Error uploading image:', error);
        });
    }
   
  };

  return (
    <>
      <Wrapper>
        <div style={{}}>
          <h2 className="mb-5 text-center">Click Your Picture</h2>
          <div style={{ height: '60vvh', margin: '20px 0' }}>
            {picture === '' ? (
              <Webcam
                audio={false}
                height={300}
                ref={webcamRef}
                width={300}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
              />
            ) : (
              <img src={picture} alt="Captured" />
            )}
          </div>
          <div style={{}}>
            {picture !== '' ? (
              <>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    setPicture('');
                  }}
                  className="btn btn-primary"
                >
                  Retake
                </button>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    sendImageToServer(); // Call the function to send the image to the server
                  }}
                  className="btn btn-primary my-4"
                  style={{ marginLeft: '20px' }}
                  
                >
                  Done
                </button>
                <ClipboardCopy copyText={picture} />
              </>
            ) : (
              <button
                onClick={(e) => {
                  e.preventDefault();
                  capture();
                }}
                className="btn btn-danger"
              >
                Capture
              </button>
            )}
          </div>
        </div>
      </Wrapper>
    </>
  );
};

export default Stats;



// import React, { useState } from 'react';
// import Webcam from 'react-webcam';
// import { CopyToClipboard } from 'react-copy-to-clipboard';
// import ClipboardCopy from './CopyText';
// import axios from 'axios'; // Import Axios
// import Wrapper from '../assets/wrappers/Dashboard';

// const WebcamComponent = () => <Webcam />;
// const videoConstraints = {
//   width: 400,
//   height: 400,
//   facingMode: 'user',
// };

// const Stats = () => {
//   const [picture, setPicture] = useState('');
//   const [showConvertButton, setShowConvertButton] = useState(false); // State to control the visibility of "Convert to Text" button
//   const [convertedText, setConvertedText] = useState(''); // State to store converted text
//   const webcamRef = React.useRef(null);

//   const capture = React.useCallback(() => {
//     const pictureSrc = webcamRef.current.getScreenshot();
//     setPicture(pictureSrc);
//     console.log(pictureSrc);
//   }, []);

//   const sendImageToServer = () => {
//     if (picture) {
//       const apiUrl = 'https://your-server-api-url.com/upload-image';
//       const formData = new FormData();
//       formData.append('image', picture);

//       axios
//         .post(apiUrl, formData, {
//           headers: {
//             'Content-Type': 'multipart/form-data',
//           },
//         })
//         .then((response) => {
//           console.log('Image uploaded successfully!', response.data);
//           setConvertedText(response.data);
//           setShowConvertButton(true); // Show the "Convert to Text" button after successful upload
//         })
//         .catch((error) => {
//           console.error('Error uploading image:', error);
//         });
//     }
//   };

//   // Function to fetch text data when the "Convert to Text" button is clicked
//   const convertToText = () => {
//     // Assuming you have an API endpoint for text conversion like 'https://your-server-api-url.com/convert-to-text'
//     axios
//       .get('https://your-server-api-url.com/convert-to-text')
//       .then((response) => {
//         console.log('Text converted successfully!', response.data);
//         setConvertedText(response.data);
//         setShowConvertButton(false); // Hide the "Convert to Text" button after successful conversion
//       })
//       .catch((error) => {
//         console.error('Error converting to text:', error);
//       });
//   };

//   return (
//     <>
//       <Wrapper>
//         <div style={{}}>
//           <h2 className="mb-5 text-center">Click Your Picture</h2>
//           <div style={{ height: '60vvh', margin: '20px 0' }}>
//             {picture === '' ? (
//               <Webcam
//                 audio={false}
//                 height={300}
//                 ref={webcamRef}
//                 width={300}
//                 screenshotFormat="image/jpeg"
//                 videoConstraints={videoConstraints}
//               />
//             ) : (
//               <img src={picture} alt="Captured" />
//             )}
//           </div>
//           <div style={{}}>
//             {picture !== '' ? (
//               <>
//                 <button
//                   onClick={(e) => {
//                     e.preventDefault();
//                     setPicture('');
//                     setShowConvertButton(false); // Hide the "Convert to Text" button when retaking the picture
//                   }}
//                   className="btn btn-primary"
//                 >
//                   Retake
//                 </button>
//                 <button
//                   onClick={(e) => {
//                     e.preventDefault();
//                     sendImageToServer();
//                   }}
//                   className="btn btn-primary my-4"
//                   style={{ marginLeft: '20px' }}
//                 >
//                   Done
//                 </button>
//                 {showConvertButton && (
//                   <button
//                     onClick={(e) => {
//                       e.preventDefault();
//                       convertToText();
//                     }}
//                     className="btn btn-success my-4"
//                     style={{ marginLeft: '20px' }}
//                   >
//                     Convert to Text
//                   </button>
//                 )}
//               </>
//             ) : (
//               <button
//                 onClick={(e) => {
//                   e.preventDefault();
//                   capture();
//                 }}
//                 className="btn btn-danger"
//               >
//                 Capture
//               </button>
//             )}
//           </div>
//         </div>
//         {convertedText && <ClipboardCopy copyText={convertedText} />}
//       </Wrapper>
//     </>
//   );
// };

// export default Stats;

