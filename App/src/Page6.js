import React from "react";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import {Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import { useState, useEffect } from "react"; // Import useState and useEffect
import backgroundImage from './background1.jpg';
import genericImage from './moisture.png';




const Page6 = () => {
    const [products, setProducts] = useState([]); // Initialize state for products
     
    

    // Fetch recommendations when the component mounts
    useEffect(() => {
        const price = localStorage.getItem('price');
        const skin_type = localStorage.getItem('skinType');
        const skin_concern = localStorage.getItem('skinConcern');

        async function fetchRecommendations() {

            try {
                const response = await fetch(`https://m10r1es0r9.execute-api.us-west-2.amazonaws.com/ailahack/recommender`, {
                    method: 'POST', // Use the appropriate HTTP method
                    body: JSON.stringify({
                        "users": [
                          {
                            "id": "user1",
                            "preferences": {
                              "product": {
                                "type": "skincare",
                                "category": "moisturizer"
                              },
                              "specifications": {
                                "skin_type": skin_type,
                                "skin_concern": skin_concern,
                                "organic": true,
                                "budget": price,
                                "specific_preference": ""
                              }
                            }
                          }
                        ]
                      })
                });

   
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
               
                
                const data = await response.json();
                console.log(data)
               

                const recommendations = data.recommendations.user1.products; // Access products for user1
                if (recommendations) {
                    setProducts(recommendations); // Set the products state directly
                    console.log(recommendations);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        fetchRecommendations(); // Call the fetch function
    }, []); // Empty dependency array ensures this runs once on mount
   
   

    return (
      
        <Box 
        sx={{ 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center', 
            justifyContent: 'center', 
            p: 3, 
            gap: 4,

            backgroundImage: `url(${backgroundImage})`, // Set the background image
            backgroundSize: 'cover', // Ensure the background covers the entire container
            backgroundPosition: 'center', // Center the background image
            backgroundRepeat: 'no-repeat', // Prevents the background from repeating
        }}
    >    
        
        
        
        {products.map((product) => (
            <Box 
            
                key={product.product_id} 
                sx={{ 
                    textAlign: 'center', 
                    maxWidth: '600px', 
                    p: 3, 
                    border: '1px solid #ddd', 
                    borderRadius: '8px', 
                    boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
                    backgroundColor: '#fff',
                }}
            >
                <Typography variant="h3" gutterBottom align="center"  sx={{ fontFamily: "Futura"}}>
                    We've handpicked your ideal moisturizer!
                </Typography>
    
                {/* Product Image */}
                <img 
                    src= {genericImage}
                    alt="product" 
                    style={{ width: '50%', height: '50%', borderRadius: '8px', marginBottom: '10px' }}
                />
    
                {/* Product Name */}
                <Typography variant="h5" gutterBottom>
                    {product.name}
                </Typography>
    
                {/* Price */}
                <Typography variant="h6" color="textSecondary" gutterBottom>
                    Price: {product.price}
                </Typography>


                {/* Affiliate Text */}
                <Box sx={{ mt: 2, p: 2, backgroundColor: '#f9f9f9', borderRadius: '8px',  marginBottom: '10px' , boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.2)'}}>
                    <Typography variant="h5" align="center">
                        <strong> Ready to lock in your perfect </strong>

                    </Typography>
                    <Typography variant="h5" align="center">
                        
                    <strong>moisturizer and earn rewards?</strong>
                    </Typography>
               
                    <Typography variant="body1" align="center" sx={{ mt: 1 }}>
                        Purchase through these links to start earning 50% of the affiliate revenue! Plus, when you leave a review, you’ll unlock even more points. Grab your personalized product and get rewarded today!
                        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 ,gap: 2}}>
                        <Button 
                        variant="contained" 
                        sx={{ 
                            backgroundColor: '#b897c2', // Button background color
                            color: 'white', // Optional: text color
                            '&:hover': {
                                backgroundColor: '#a278b3', // Optional: darker shade for hover effect
                            }
                        }}
                        onClick={(e) => {e.preventDefault(); window.location.href = "https://www.sephora.com/";}}
                        >
                        Shop Sephora
                         </Button>
                        
                        <Button 
                        variant="contained" 
                        sx={{ 
                            backgroundColor: '#b897c2', // Button background color
                            color: 'white', // Optional: text color
                            '&:hover': {
                                backgroundColor: '#a278b3', // Optional: darker shade for hover effect
                            }
                        }}
                        onClick={(e) => {e.preventDefault(); window.location.href = "https://www.ulta.com/";}}
                        >
                        Shop Ulta
                         </Button>
                        </Box>
                    </Typography>
                </Box>
           
                {/* Product Description */}
                <Typography variant="body1" align="center" sx={{ mb: 2 }}>
                    {product.description}
                </Typography>
    
                
    
                
    
            </Box>
        ))}
    </Box>
    
    );
};


export default Page6;
