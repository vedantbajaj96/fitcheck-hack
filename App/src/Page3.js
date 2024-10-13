import React from "react";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import {Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Page3 = () => {
    const [skinType, setSkinType] = React.useState('');
    const navigate = useNavigate();

    const goToNextPage = () => {
        navigate('/page2'); // Navigates to Page3
    };

    const handleChange = (event) => {
        const value = event.target.value;
        setSkinType(value);
        localStorage.setItem('skinType', value); // Save skin type value to local storage
        console.log(skinType)
    };
    
  
    return (
      <Box sx={{
        display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh', // Ensures full viewport height for vertical centering
          backgroundColor: 'lightblue', // Add light blue background color here
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
            Select Skin Type
            </Typography>

            <Typography variant="h6" component="h6" color="#404040" sx={{ mb: 4 , fontFamily: 'Helvetica'  }}>
            Your skin’s unique—your skincare should be too. Tell us about your skin type, and we’ll curate personalized recommendations just for you.
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

            <InputLabel id="demo-simple-select-label">Skin Type</InputLabel>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={skinType}
                label="Skin Type"
                onChange={(e) => { handleChange(e); goToNextPage(); }} // Save the value and navigate
                
            >

                <MenuItem value={'Oily'} > Oily: Skin tends to produce excess oil, often shiny.</MenuItem>
                <MenuItem value={'Dry'} >Dry: Skin feels tight or flaky, lacks moisture.</MenuItem>
                <MenuItem value={'Combination'} >Combination: Oily in some areas (e.g., T-zone) and dry in others.</MenuItem>
                <MenuItem value={'Normal'} >Normal: Balanced skin, not too oily or dry.</MenuItem>
               

            </Select>
            </FormControl>
        </Box>
        </Box>
    );

};

export default Page3;
