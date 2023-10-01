import React, { useState } from 'react';
import axios from 'axios';
const QRCode = require('qrcode'); // Importing the qrcode library

const MyForm = () => {
  const [formData, setFormData] = useState({
    // userId: "64fbb7c7c2f13687cbef152a",
    userName: '',
    userEmail: '',
    userMobile: '',
    city: '',
    country: '',
    address: '',
    pin: 0,
  });
  function generateUniqueHexValue(length) {
    const characters = '0123456789ABCDEF';
    let hexValue = '0x';
  
    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * characters.length);
      hexValue += characters[randomIndex];
    }
  
    return hexValue;
  }
  
  // Usage:
  const uniqueHexValue = generateUniqueHexValue(6); // Change 6 to your desired length
  console.log(uniqueHexValue);
  
  const [qrCodeData, setQrCodeData] = useState(''); // State to store QR code data

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Get the verificationId from products in formData
    // const verificationId = formData.products.verificationId;

    // Create a string containing the username and verificationId
    const qrCodeText = `UserName: ${formData.userName}\nVerificationId: ${uniqueHexValue}`;

    // Generate the QR code
    try {
      const qrCodeDataURL = await QRCode.toDataURL(qrCodeText);

      // Set the QR code data URL in the state
      setQrCodeData(qrCodeDataURL);
    } catch (error) {
      console.error(error);
    }

    // Send form data to the API (you can keep your existing code for this)
    const options = {
      method: 'POST',
      url: 'http://127.0.0.1:8000/order/ecommerce/',
      headers: { 'Content-Type': 'application/json' },
      data: {
        userId: "64fbb7c7c2f13687cbef152a",
        userName: formData.userName,
        userEmail: formData.userEmail,
        userMobile: formData.userMobile,
        city: formData.city,
        country: formData.country,
        actress: formData.address,
        pin: formData.pin,
        products: {
          productImage: "string",
          quantity: "234",
          color: "Green",
          size: "XL",
          quality: "Cotton",
          verificationId: uniqueHexValue.toString(),
        },
      },
    };

    axios
      .request(options)
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.error(error);
      });
  };

  return (
    <div className="my-form-container mx-auto max-w-lg p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">Please Enter the Following Details</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key} className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">
              {key.charAt(0).toUpperCase() + key.slice(1)}:
              <input
                type="text"
                name={key}
                value={formData[key]}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              />
            </label>
          </div>
        ))}
        <button type="submit" className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600">
          Submit
        </button>
      </form>

      {/* Display the QR code if qrCodeData is not empty */}
      {qrCodeData && (
        <div className="mt-6">
          <h2 className="text-2xl font-semibold mb-4">QR Code</h2>
          <img src={qrCodeData} alt="QR Code" className="w-full" />
        </div>
      )}
    </div>
  );
};

export default MyForm;