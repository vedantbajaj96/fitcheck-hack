import React from "react";
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import b1 from './1.png';
import b2 from './2.png';
import b3 from './3.png';
import b4 from './4.png';
import b5 from './5.png';

const Page7 = () => {
    const [skinType, setSkinType] = React.useState('');
    const navigate = useNavigate();

    const goToNextPage = () => {
        navigate('/page4'); 
    };

    const handleChange = (event) => {
        const value = event.target.value;
        setSkinType(value);
        localStorage.setItem('skinType', value); // Save skin type value to local storage
        console.log(skinType)
    };

    return (
        <Box 
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100vh', // Full viewport height for vertical centering
                padding: 3,
                backgroundColor: '#C3B1E1' // Add light blue background color here
            }}
        >
            {/* Header */}
            <Typography variant="h4" component="h1" fontWeight="bold" color="WHITE" sx={{ mb: 4 }}>
                Choose Your Product
            </Typography>

            {/* Images Row */}
            <Box 
                sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'center',
                    alignItems: 'center',
                    gap: 2, // Space between images
                    flexWrap: 'wrap', // Wraps the images if screen is too narrow
                }}
            >
                <img src={b1} alt="Product 1" style={{ width: '180px', height: 'auto', cursor: 'pointer' }} />
                <img src={b2} alt="Product 2" style={{ width: '180px', height: 'auto', cursor: 'pointer' }} />
                <img src={b3} alt="Product 3" style={{ width: '180px', height: 'auto', cursor: 'pointer' }} />
                <img src={b4} alt="Product 4" style={{ width: '180px', height: 'auto', cursor: 'pointer' }} />
                <img src={b5} alt="Product 5" style={{ width: '180px', height: 'auto', cursor: 'pointer' }} />
            </Box>
        </Box>
    );
};

export default Page7;
