import React from "react";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import backgroundImage from './background3.jpg';

const Page2 = () => {
    const [price, setPrice] = React.useState('');
    const navigate = useNavigate();

    const handleChange = (event) => {
        const value = event.target.value;
        setPrice(value);
        localStorage.setItem('price', value); // Save price value to local storage
    };

    const goToNextPage = () => {
        navigate('/page6'); // Navigates to Page3
    };

    return (
        <Box sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh', // Ensures full viewport height for vertical centering
            backgroundColor: '#C1E1C1', // Add light blue background color here
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
                boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.4)',
                backgroundColor: '#FAFAFA', 
            }}
            >

            <Typography variant="h3" component="h3" color="black" sx={{ mb: 3, fontFamily: 'Futura'  }}>
                Select Your Price Range
            </Typography>

            <Typography variant="h6" component="h6" color="#404040" sx={{ mb: 4 , fontFamily: 'Helvetica'  }}>
            Beauty on any budget. Select your price range and we’ll tailor recommendations that fit your wallet without compromising on quality.
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

                <InputLabel id="price-select-label">Price Range</InputLabel>
                <Select
                    labelId="price-select-label"
                    id="price-select"
                    value={price}
                    label="Price Range"
                    onChange={(e) => { handleChange(e); goToNextPage(); }} // Save the value and navigate
                >
                    <MenuItem value={20}>$5 - $20 (Drugstore Range)</MenuItem>
                    <MenuItem value={50}>$21 - $50 (Mid-Range)</MenuItem>
                    <MenuItem value={100}>$51 - $100 (Premium Range)</MenuItem>
                    <MenuItem value={1000}>$100+ (Luxury Range)</MenuItem>
                </Select>
            </FormControl>
            </Box>
        </Box>
    );
};

export default Page2;
