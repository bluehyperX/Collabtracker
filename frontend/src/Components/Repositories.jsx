import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HeatmapCard from '../heatmap_cards/heatmap_card_repo.jsx';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { DataGrid } from '@mui/x-data-grid';
import Grid from '@mui/material/Grid';
import { Typography } from '@mui/material';

const convertToIST = (isoDate) => {
    const date = new Date(isoDate);
    if (!isNaN(date)) {
        return date.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
    } else {
        return isoDate;
    }
};

const Repositories = ({ selectedYear }) => {
    const [data, setData] = useState(null);
    const [most_active_repo_rows, set_most_active_repo_rows] = useState([]);
    const [least_active_repo_rows, set_least_active_repo_rows] = useState([]);

    useEffect(() => {
        const fetch_request = async () => {
            const result = await axios.get(`http://localhost:8000/repo_data/?year=${selectedYear}`);
            setData(result.data);
            const most_active_repos_result = await axios.get("http://localhost:8000/most_active_repos");
            set_most_active_repo_rows(most_active_repos_result.data);
            const least_active_repos_result = await axios.get("http://localhost:8000/least_active_repos");
            set_least_active_repo_rows(least_active_repos_result.data);
        };
        fetch_request();
    }, [selectedYear]);

    const columns = [
        { field: 'id', headerName: 'S. No.', width: 50, valueGetter: (value, row) => value },
        { field: 'repository_name', headerName: 'Repo Name', width: 190 },
        { field: 'total_commits', headerName: 'Total Commits', width: 130, type: 'number' },
        { field: 'last_commit', headerName: 'Last Commit', width: 200 },
    ];

    most_active_repo_rows.forEach((row, index) => { row.id = index + 1; row.last_commit = convertToIST(row.last_commit) });
    least_active_repo_rows.forEach((row, index) => { row.id = index + 1; row.last_commit = convertToIST(row.last_commit) });

    return (
        <div>
            <div className="content">
                <Accordion className="facts">
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="h4">Cumulative Facts</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid container spacing={2}>
                            <Grid item xs={6}>
                                <Typography variant="h5">Top 3 Most Active Repositories</Typography>
                                <DataGrid
                                    rows={most_active_repo_rows}
                                    columns={columns}
                                    autoHeight
                                    hideFooter
                                />
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="h5">Top 3 Least Active Repositories</Typography>
                                <DataGrid
                                    rows={least_active_repo_rows}
                                    columns={columns}
                                    autoHeight
                                    hideFooter
                                />
                            </Grid>
                        </Grid>
                    </AccordionDetails>
                </Accordion>
                <br />
                {data && Object.keys(data.heatmap_data).map((repo, index) => (
                    <HeatmapCard
                        key={index}
                        repo_name={repo}
                        heatmap_data={data.heatmap_data[repo]}
                        heatmap_dates={data.heatmap_dates}
                        branch_data={data.branch_data[repo]}
                        user_data={data.user_data[repo]}
                        file_data={data.file_data[repo]}
                        average_commits_per_day={data.average_commits_per_day[repo]}
                        total_branches={data.total_branches[repo]}
                        last_active_branch={data.last_active_branch[repo]}
                        total_users={data.total_users[repo]}
                        last_active_user={data.last_active_user[repo]}
                        last_commits={data.last_commit_datetime[repo]}
                        last_changed_files={data.last_changed_file[repo]}
                        max_file_changed={data.max_changed_files_in_commit[repo]}
                        avg_file_changed={data.avg_changed_files_in_commit[repo]}
                        max_changes={data.max_changes_in_file_in_commit[repo]}
                        avg_changes={data.avg_changes_in_file_in_commit[repo]}
                    />
                ))}
            </div>
        </div>
    );
};

export default Repositories;
