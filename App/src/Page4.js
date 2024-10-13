import React from "react";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import {Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react"; // Import useState and useEffect

const Page4 = () => {
    const [skinConcern, setSkinConcern] = React.useState('');
     

    const handleChange = (event) => {
        const value = event.target.value;
        setSkinConcern(value);
        localStorage.setItem('skinConcern', value); // Save price value to local storage
        console.log(skinConcern)
    };
    const navigate = useNavigate();

    const goToNextPage = () => {
        navigate('/page3'); // Navigates to Page5
    };
  
    return (

        
      <Box sx={{
        display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh', // Ensures full viewport height for vertical centering
          backgroundColor: '#C3B1E1', // Add light blue background color here
          
      }}
      flexDirection="column"
      >
        <Box 
            sx={{ 
                textAlign: 'center', 
                maxWidth: '650px', 
                p: 3, 
                border: 'px solid #ddd', 
                borderRadius: '8px', 
                boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.2)',
                backgroundColor: '#FAFAFA', 
            }}
            >
        <Typography variant="h3" component="h3" color="black" sx={{ mb: 3, fontFamily: 'Futura'  }}>
        Select Skin Concern
        </Typography>

        <Typography variant="h6" component="h6" color="#404040" sx={{ mb: 4 , fontFamily: 'Helvetica'  }}>
        Let’s start by understanding your skin. What’s your main concern? Choose from the options below, and we’ll find the perfect match for you.
        </Typography>


        <FormControl 
                sx={{ 
                    mb: 2, 
                    minWidth: 400, 
                    bgcolor: '#f5f5f5', // Set the background color
                    border: '1px solid #404040', // Optional: Set border color
                    borderRadius: '4px' // Optional: Add some border radius
                }} 
            >

          <InputLabel id="demo-simple-select-label">Skin Concern</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={skinConcern}
            label="Skin Concern"
            onChange={(e) => { handleChange(e); goToNextPage(); }}
          >

            <MenuItem value={"Acne"}>Acne: Prone to breakouts and clogged pores.</MenuItem>
            <MenuItem value={"Dryness"}>Dryness/Dehydration: Skin feels tight or flaky, needs moisture.</MenuItem>
            <MenuItem value={"Wrinkles"}>Fine Lines/Wrinkles: Visible signs of aging.</MenuItem>
            <MenuItem value={"Hyperpigmentation"}>Hyperpigmentation/Dark Spots: Uneven skin tone, dark patches.</MenuItem>
            <MenuItem value={"Redness"}>Redness/Rosacea: Prone to redness, sensitive to irritation.</MenuItem>
            <MenuItem value={"Oil Control"}>Oil Control/Breakouts: Excess oil production, prone to shine.</MenuItem>
            <MenuItem value={"Dullness"}>Dullness/Lack of Glow: Skin lacks radiance, looks tired.</MenuItem>
            <MenuItem value={"Enlarged Pores"}>Enlarged Pores: Visible, larger pores, often in oily areas.</MenuItem>
            <MenuItem value={"Sensitive Skin"}>Sensitive Skin/Irritation: Prone to reactions from products or the environment.</MenuItem>

          </Select>
        </FormControl>
      </Box>
      </Box>
    );

};

export default Page4;
