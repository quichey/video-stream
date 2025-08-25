import Skeleton from "@mui/material/Skeleton";

export default function Loading({ height = 360 }) {
    return (
        <Skeleton 
        variant="rectangular" 
        width="100%" 
        height={height} 
        animation="wave" 
        />
    );
}