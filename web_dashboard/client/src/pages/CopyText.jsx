import { useState } from "react";
function ClipboardCopy({ copyText }) {
    const [isCopied, setIsCopied] = useState(false);
  
    // This is the function we wrote earlier
    async function copyTextToClipboard(text) {
      if ('clipboard' in navigator) {
        return await navigator.clipboard.writeText(text);
      } else {
        return document.execCommand('copy', true, text);
      }
    }
  
    // onClick handler function for the copy button
    const handleCopyClick = () => {
      // Asynchronously call copyTextToClipboard
      copyTextToClipboard(copyText)
        .then(() => {
          // If successful, update the isCopied state value
          setIsCopied(true);
          setTimeout(() => {
            setIsCopied(false);
          }, 3000);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  
    return (
        <>
      <div>
        <textarea type="text" value={copyText} readOnly  style={{width:"300px",height:"100px",marginBottom:"20px",marginTop:"20px"}}/>
        {/* Bind our handler function to the onClick button property */}
       
      </div>
       <button className="btn btn-primary" onClick={handleCopyClick}>
       <span>{isCopied ? 'Copied!' : 'Copy'}</span>
     </button>
     </>
    );
  };
  export default ClipboardCopy