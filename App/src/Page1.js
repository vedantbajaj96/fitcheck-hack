import React from "react";
import { Box, Typography } from '@mui/material';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import backgroundImage from './background2.jpg';
import { useState, useEffect } from "react"; // Import useState and useEffect

// Home page component (Get Started)
const Page1 = () => {
  const navigate = useNavigate();
  
  const goToNextPage = () => {
    navigate('/page4'); // Navigate to the next page
  };

  return (
    <Box
      sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh',  // Full viewport height for centering
        p: 3, 
        gap: 2,
        backgroundImage: `url(${backgroundImage})`, // Set the background image
        backgroundSize: 'cover', // Ensure the background covers the entire container
        backgroundPosition: 'center', // Center the background image
        backgroundRepeat: 'no-repeat', // Prevent the background from repeating
      }}
    >
      <Typography 
        variant="h2" 
        component="h1" 
        fontWeight="bold" 
        color="white" 
        sx={{ mb: 0}} // Adds margin below the heading
      >
      
        Shop Smarter. Earn More.
      </Typography>

      <Typography 
        variant="h5" component="h5" color="white" sx={{ mb: 3}}
        
      >
  
      Personalized recommendations that reward you every step of the way.
      </Typography>

     
      
       {/* Button Row */}
       <Box 
                sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexWrap: 'wrap', // Wrap the buttons to the next row
                    gap: 2, // Space between buttons
                    maxWidth: '900px', // Control the width to fit two rows
                    mt: 4,
                }}
            >
                {["Facial Moisturizers", "Dietary Supplements", "Personal Care Devices", "Makeup and Beauty", "Fitness Gear", "Healthy Snacks"].map((label, index) => (
                    <Button 
                        key={index}
                        variant="contained" 
                        sx={{ 
                            color: label === "Facial Moisturizers" ? 'white' : 'White', // White for active, gray for inactive
                            backgroundColor: label === "Facial Moisturizers" ? '#F49595' : '#555151', // Transparent for active, light gray for inactive
                            border: '2px solid white', // Makes the button rounded
                            borderRadius: '10px', // Makes the button rounded
                            width: '270px', // Sets fixed width for consistency
                            height: '50px', // Sets fixed height for consistency
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            opacity: label === "Facial Moisturizers" ? 1 : 0.2,
                        }} 
                        size="large"
                        onClick={goToNextPage}
                    >
                        {label}
                    </Button>
                ))}
            </Box>
    </Box>
  );
};

export default Page1;
