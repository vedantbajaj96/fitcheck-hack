import React from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import {Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';


const Page5 = () => {
    const [skinConcern, setSkinConcern] = React.useState('');

    const handleChange = (event) => {
      setSkinConcern(event.target.value);
    };
    const navigate = useNavigate();

    const goToNextPage = () => {
        navigate('/page6'); // Navigates to Page5
    };
  
    return (
        <Box sx={{
            display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              height: '100vh' // Ensures full viewport height for vertical centering
              
          }}
          flexDirection="column"
          >

        <Typography variant="h3" component="h3" fontWeight="bold" color="primary" sx={{ mb: 3 }}>
        Any additional preferences:
        </Typography>

        <TextField id="outlined-basic" label="Input" variant="outlined" onChange={goToNextPage} />
      </Box>
    );

};

export default Page5;
