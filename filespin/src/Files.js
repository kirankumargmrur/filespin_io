import React, { useState } from "react";
import Button from '@mui/material/Button';



function Files(){
    const [loading, setLoading] = useState(false);
    const handleFileDownload = async () => {
        setLoading(true);
        const response = await fetch('http://0.0.0.0:8080/download');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'files.zip';
        document.body.appendChild(a);
        a.click();
        setLoading(false);
    }
    
    return (
        <>
        <Button variant="contained" onClick={handleFileDownload}>{loading ? 'Downloading...' : 'Click me to Download'}</Button>
        </>
        
    );
}

export default Files