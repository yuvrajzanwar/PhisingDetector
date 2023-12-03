import React, { useState,useEffect } from 'react';
import "../styles/styles_homepage.css";



const Homepage = () => {
  const [status,setStatus] =useState("processed");
  //no-input,processing,processed.
  const [verdict,setVerdict] = useState("secure");
  //secure,suspicious(or unsafe)
  const [tab, setTab] = useState("url");
  //url or email
  const [url, setUrl] =useState('');

  const [subject, setSubject] = useState('');
  const [sender, setSender] = useState('');
  const [date, setDate] = useState('');
  const [body, setBody] = useState('');

  const handleInputChange = (e) => {
    setUrl(e.target.value);
  };

  function showVerdictLogo() {
    if(status === "processed")
    {
      if(verdict === "secure")
          return `${process.env.PUBLIC_URL}/Correct.png` ;
      if(verdict === "suspicious")
          return `${process.env.PUBLIC_URL}/Danger.png` ;
      if (verdict === "invalid")
      return "";  
    }

    if(status==="processing")
    return `${process.env.PUBLIC_URL}/loading.gif`;

    return "";
  }

  function showVerdictText() {
    if (status === "processed") {
      if (verdict === "secure")
        return "Secure";
      if (verdict === "suspicious")
        return "Suspicious";
      if (verdict === "invalid")
        return "Invalid Link"; 
    }
    if (status === "processing")
      return "Processing";
    if (status === "no-input")
      return "";
  
    return ""; // Default case
  }
  
  
  const checkPhishing = async () => {
    try {
      const response = await fetch('http://your-django-api-url/check-phishing', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      
      const data = await response.json();

      // Update the UI based on the phishing detection result
      setStatus(data.status);


    } catch (error) {
      console.error('Error checking phishing status:', error);
    }
  };

  
  const extractCurrentUrl = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentUrl = tabs[0].url;
      if(currentUrl !== 'chrome://newtab/')
        setUrl(currentUrl);
      console.log('Current URL:', currentUrl);
    });
  };


  useEffect(() => {
    // Call the function to extract the current URL on component mount
      extractCurrentUrl();
  }, []);

  const Emailbody = () =>{


    useEffect(() => {
      console.log("first");
      // Function to check if the current page is a Gmail email
      function isGmailEmail() {
        return window.location.href.includes('mail.google.com') && document.querySelector('h2.hP') !== null;
      }
  
      // Check if chrome is defined (running in a Chrome extension context)
      if (typeof chrome !== 'undefined' && chrome.runtime) {
        // Use chrome.tabs.query to get information about the active tab
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const activeTab = tabs[0];
          console.log("Inside if");
          // Use chrome.tabs.sendMessage to request email content from content.js
          chrome.tabs.sendMessage(activeTab.id, { message: 'getGmailEmailContent' }, (response) => {
            if (response) {
              console.log("Response");
              setSubject(response.subject);
              setSender(response.sender);
              setDate(response.date);
              console.log(response.subject);
            }
            console.log("Okay");
          });
        });
      } else {
        console.warn('Chrome extension context not detected.');
      }
    }, []);
      // // Check if chrome is defined (running in a Chrome extension context)
      // if ( typeof chrome !== 'undefined' && chrome.runtime) {
      //   // process.env.REACT_APP_CHROME_EXTENSION === 'true' &&
      //   // Use chrome.runtime.sendMessage to request email content from your extension scripts
      //   chrome.runtime.sendMessage({ message: 'getGmailEmailContent' }, (response) => {
      //     if (response && response.subject && response.sender && response.date) {
      //       setSubject(response.subject);
      //       setSender(response.sender);
      //       setDate(response.date);
      //     }
      //   });
      // } else {
      //   // Handle the case when chrome is not defined (not running in a Chrome extension context)
      //   console.warn('Chrome extension context not detected.');
      // }
    
    
    return(
    <>
    <div className='email-body'>
        <div className='height-setter'>
          <div className='info-table'>
            <table>
              <tr>
                <td><strong>Subject:{subject}</strong></td>
              </tr>
              <tr>
                <td><strong>Sender:{sender}</strong></td>
              </tr>
              <tr>
              <td><strong>Date:{date}</strong></td>
              </tr>
            </table>
          </div>
          <div className='verdict'>
            <div className='verdict-logo'>
            <img
              src={showVerdictLogo()}
              alt={showVerdictText()}
              style={{ height: '5rem',
              }}
            />
            </div>
            <div className='verdict-text-container'>
              <div className='verdict-text'>{showVerdictText()}</div>
            </div>
          </div>
        </div>
        <div className='description'>Our Extension does real-time analysis to check if the provided Email is a legitimate one
        </div>
        
      </div>
    </>
    )
  }
  return (
    <>
    <div className='outer-container'>
    <div className='logoandtitle'>
      <div className='logo'></div>
      <div className='title'><strong>Web</strong>Sentinel</div>
    </div>

    <div className='tabs'>
      <button 
      className='tabs-button' 
      onClick={()=>{setTab("url");
      }}
      style={{
        backgroundColor: tab==="url" ? '#B2E3FF' : 'white',
        border: '1px solid #ccc',
        cursor: 'pointer',
        transition: 'background-color 0.3s, color 0.3s',
      }}>URLs
      </button>

      <button 
      className='tabs-button' 
      onClick={()=>{setTab("email");
      }}
      style={{
        backgroundColor: tab==="email" ? '#B2E3FF' : 'white',
        border: '1px solid #ccc',
        cursor: 'pointer',
        transition: 'background-color 0.3s, color 0.3s',
      }}>Email
      </button>
    </div>
    <div>
      {/* {(tab === "link")? <Urlbody/> : <Emailbody/>} */}
      {tab === "url" ? (
        <>
          <div className='url-body'>
          <div className='height-setter'>
            <div className='upper-title'>Enter a URL below to check its authenticity</div>
            <div>
              <input type='text' 
                name='link' 
                className='input-link' 
                placeholder='Enter the link here'
                value={url}
                onChange={handleInputChange}
              />
            </div>
            <div className='search-button'><button>Check</button></div>
            <div className='verdict'>
              <div className='verdict-logo'>
              <img
                src={showVerdictLogo()}
                alt={showVerdictText}
                style={{ height: '5rem',
                }}
              />
              </div>
              <div className='verdict-text-container'>
                <div className='verdict-text'>{showVerdictText()}</div>
              </div>
            </div>
            </div>
            <div className='description'>Our Extension does real-time analysis to check if the provided URL is a phishing one</div>
          </div>
        </>
        )
      :
        <Emailbody/>
      }
    </div>
    </div>
    </>
  )
}

export default Homepage