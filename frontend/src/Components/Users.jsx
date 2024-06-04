import React, { useState,useEffect } from 'react'
import axios from 'axios' 
import Header from '../header/header.jsx'
import HeatmapCard from '../heatmap_cards/heatmap_card_user.jsx'
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { DataGrid } from '@mui/x-data-grid';
import { Typography } from '@mui/material';
import Grid from '@mui/material/Grid';

const Repositories = () => 
{
    const [data,setData] = useState(null)
    const [most_active_user_total_rows,set_most_active_user_total_rows] = useState([])
    const [most_active_user_consistency_rows,set_most_active_user_consistency_rows] = useState([])
    const [most_productive_days_rows,set_most_productive_days_rows] = useState([])

    useEffect(() => 
    {
        const fetch_request = async () =>
        {
            const result = await axios.get("http://localhost:8000/user_data")
            setData(result.data)  
            //set_most_active_user_total_rows(result.data)
            //set_most_active_user_consistency_rows(result.data)
            //set_most_productive_days_rows(result.data)
            console.log(result)
        }
        fetch_request();
    },[])


    const most_active_user_total_columns = [
        { field: 'sno', headerName: 'S. No.', width: 70, valueGetter: (value,row) => value },
        { field: 'user', headerName: 'User Name', width: 130 },
        { field: 'commits', headerName: 'Total Commits', width:130, type:'number' },
        { field: 'last_commit', headerName: 'Last Commit', width:130, type:'date' },
      ];

    const most_active_user_consistency_columns = [
      { field: 'sno', headerName: 'S. No.', width: 70, valueGetter: (value,row) => value },
      { field: 'user', headerName: 'User Name', width: 130 },
      { field: 'commits_per_week', headerName: 'Commits/Week', width:130, type:'number' },
      { field: 'last_commit', headerName: 'Last Commit', width:130, type:'date' },
    ];

    const most_productive_days_columns = [
        { field: 'sno', headerName: 'S. No.', width: 70 },
        { field: 'day', headerName: 'Day', width: 130 },
        { field: 'commits', headerName: 'Total Commits', width:130, type:'number' },
      ];  


  return (
    <div>
        <Header/><div className="content">
        <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h4">Facts</Typography>
            </AccordionSummary>
            <AccordionDetails>
            <Grid container spacing={4}>
                <Grid item xs={6}>
                    <Typography variant="h5">Top 3 Most Active Users (Total Commits)</Typography>
                    <DataGrid
                      rows={most_active_user_total_rows}
                      columns={most_active_user_total_columns}
                      autoHeight
                      hideFooterPagination
                    />
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="h5">Top 3 Most Active Users (Consistency)</Typography>
                    <DataGrid
                        rows={most_active_user_consistency_rows}
                        columns={most_active_user_consistency_columns}
                        autoHeight
                        hideFooterPagination
                    />
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="h5">Top 3 Most Productive Days</Typography>
                    <DataGrid
                        rows={most_productive_days_rows}
                        columns={most_productive_days_columns}
                        autoHeight
                        hideFooterPagination
                    />
                </Grid>
            </Grid>
            </AccordionDetails>
        </Accordion>
        <br></br>
        {
            data && Object.keys(data.heatmap_data).map((user,index) => 
                (
                    <HeatmapCard 
                    key={index}
                    heatmap_data={data.heatmap_data[user]}
                    user_name={user}
                    heatmap_dates={data.heatmap_dates}
                    top_repositories={data.top_repositories[user]}
                    most_productive_days={data.most_productive_days[user]}/>
                ))
        }   
        </div>       
    </div>
  )
}

export default Repositories