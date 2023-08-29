import React, { useState } from "react";
import ClipboardCopy from "./CopyText";

const UploadAndDisplayImage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [base64Image, setBase64Image] = useState(null);

  const handleImageChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      const reader = new FileReader();

      reader.onload = (e) => {
        // The result attribute contains the base64-encoded image data
        const base64Data = e.target.result;

        // Console log the base64 encoding
        console.log(base64Data);

        setSelectedImage(selectedFile);
        setBase64Image(base64Data);
      };

      // Read the selected file as a data URL (base64)
      reader.readAsDataURL(selectedFile);
    }
  };

  return (
    <div>
      <h2>Upload Picture</h2>

      {selectedImage && (
        <div>
          <img alt="not found" width={"250px"} src={URL.createObjectURL(selectedImage)} />
          <br />
          <button style={{marginTop:"20px"}} className="btn btn-primary" onClick={() => { setSelectedImage(null); setBase64Image(null); }}>Remove</button>
        </div>
      )}

      <br />
      <br />

      <input
        type="file"
        name="myImage"
        onChange={handleImageChange}
      />
      
      {/* Pass the base64Data variable to the ClipboardCopy component */}
      {base64Image && <ClipboardCopy copyText={base64Image} />}
      
    </div>
  );
};

export default UploadAndDisplayImage;





// import React from "react";

// class UploadAndDisplayImage extends React.Component {
//   state = {
//     file: null,
//     base64URL: ""
//   };

//   getBase64 = file => {
//     return new Promise(resolve => {
//       let fileInfo;
//       let baseURL = "";
//       // Make new FileReader
//       let reader = new FileReader();

//       // Convert the file to base64 text
//       reader.readAsDataURL(file);

//       // on reader load somthing...
//       reader.onload = () => {
//         // Make a fileInfo Object
//         console.log("Called", reader);
//         baseURL = reader.result;
//         console.log(baseURL);
//         resolve(baseURL);
//       };
//       console.log(fileInfo);
//     });
//   };

//   handleFileInputChange = e => {
//     console.log(e.target.files[0]);
//     let { file } = this.state;

//     file = e.target.files[0];

//     this.getBase64(file)
//       .then(result => {
//         file["base64"] = result;
//         console.log("File Is", file);
//         this.setState({
//           base64URL: result,
//           file
//         });
//       })
//       .catch(err => {
//         console.log(err);
//       });

//     this.setState({
//       file: e.target.files[0]
//     });
//   };

//   render() {
//     return (
//       <div><img src={this.state} alt="" />
//         <input type="file" name="file" onChange={this.handleFileInputChange} />
//       </div>
//     );
//   }
// }

// export default UploadAndDisplayImage;
