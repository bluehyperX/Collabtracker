import React from 'react';
import Tooltip from '@uiw/react-tooltip';
import HeatMap from '@uiw/react-heat-map';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { DataGrid } from '@mui/x-data-grid';
import Grid from '@mui/material/Grid';
import { Typography } from '@mui/material';
import './heatmap_card.css';
// Helper function to convert ISO date to IST with both date and time
const convertToIST = (isoDate) => {
  const date = new Date(isoDate);
  return date.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
};

const Heatmap_Card_Repo = (props) => {
    const repo_name = props.repo_name;
    const heatmap_info = props.heatmap_data;
    const startDate = props.heatmap_dates.startDate;
    const endDate = props.heatmap_dates.endDate;
    const most_active_branches_rows = props.branch_data
    const most_active_users_rows = props.user_data
    const most_frequently_changed_files_rows = props.file_data
    const avg_commits = props.average_commits_per_day;
    const total_branches = props.total_branches;
    const last_active_branch = props.last_active_branch;
    const total_users = props.total_users;
    const last_active_user = props.last_active_user;
    const last_commits = props.last_commits;
    const last_changed_files = props.last_changed_files;
    const max_file_changed = props.max_file_changed;
    const avg_file_changed = props.avg_file_changed;
    const max_changes_in_file_in_commit = props.max_changes;
    const avg_changes_in_file_in_commit = props.avg_changes;

    const most_active_branches_columns = [
        { field: 'id', headerName: 'S. No.', width: 70, valueGetter: (value,row) => value },
        { field: 'branch__name', headerName: 'Branch Name', width: 130 },
        { field: 'total_commits', headerName: 'Total Commits', width: 130, type: 'number' },
        { field: 'last_commit', headerName: 'Last Commit', width: 200 },
    ];

    const most_active_users_columns = [
        { field: 'id', headerName: 'S. No.', width: 70, valueGetter: (value,row) => value },
        { field: 'authors__name', headerName: 'User Name', width: 130 },
        { field: 'total_commits', headerName: 'Total Commits', width: 130, type: 'number' },
        { field: 'last_commit', headerName: 'Last Commit', width: 200 },
    ];

    const most_frequently_changed_files_columns = [
        { field: 'id', headerName: 'S. No.', width: 70, valueGetter: (value,row) => value },
        { field: 'files__name', headerName: 'File Name', width: 130 },
        { field: 'total_commits', headerName: 'Total Commits', width: 130, type: 'number' },
        { field: 'last_commit', headerName: 'Last Commit', width: 200 },
    ];

    // Ensure each row has a unique `id` field for DataGrid
    most_active_branches_rows.forEach((row, index) => (row.id = index + 1, row.last_commit = convertToIST(row.last_commit)));
    most_active_users_rows.forEach((row, index) => (row.id = index + 1, row.last_commit = convertToIST(row.last_commit)));
    most_frequently_changed_files_rows.forEach((row, index) => (row.id = index + 1, row.last_commit = convertToIST(row.last_commit)));

    return (
        <div className="card">
            <h2>{repo_name}</h2>
            <HeatMap
                value={heatmap_info}
                width={1200}
                height={200}
                rectSize={20}
                startDate={new Date(startDate)}
                endDate={new Date(endDate)}
                rectRender={(props, data) => {
                    return (
                        <Tooltip placement="top" content={`commit(s): ${data.count || 0}, date: ${data.date}`}>
                            <rect {...props} />
                        </Tooltip>
                    );
                }}
            />
            <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="h5">Facts</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Grid container spacing={2}>
                        <Grid item xs={6}>
                            <Typography variant="h7">Total Branches: {total_branches}</Typography>
                            <br />
                            <Typography variant="h7">Total Users: {total_users}</Typography>
                            <br />
                            <Typography variant="h7">
                                Last Active Branch: {last_active_branch.branch__name} @ {convertToIST(last_active_branch.last_commit)}
                            </Typography>
                            <br />
                            <Typography variant="h7">
                                Last Active User: {last_active_user.authors__name} @ {convertToIST(last_active_user.last_commit)}
                            </Typography>
                            <br />
                            <Typography variant="h7">
                                Last Changed File: {last_changed_files.files__name} @ {convertToIST(last_changed_files.last_commit)}
                            </Typography>
                            <br />
                            <Typography variant="h7">Average Commits/Day in 30 days: {avg_commits}</Typography>
                            <br />
                            <Typography variant="h7">Last Commit: {convertToIST(last_commits)}</Typography>
                            <br />
                            <Typography variant="h7">Max number of changed files in a commit: {max_file_changed}</Typography>
                            <br />
                            <Typography variant="h7">Avg number of changed files in a commit: {avg_file_changed}</Typography>
                            <br />
                            <Typography variant="h7">Max number of changes in a file: {max_changes_in_file_in_commit}</Typography>
                            <br />
                            <Typography variant="h7">Avg number of changes in a file: {avg_changes_in_file_in_commit}</Typography>
                            <br />
                        </Grid>
                        <Grid item xs={6}>
                            <Typography variant="h6">Top 3 Most Active Branches</Typography>
                            <DataGrid
                                rows={most_active_branches_rows}
                                columns={most_active_branches_columns}
                                autoHeight
                                hideFooter
                                getRowId={(row) => row.id}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <Typography variant="h6">Top 3 Most Active Users</Typography>
                            <DataGrid
                                rows={most_active_users_rows}
                                columns={most_active_users_columns}
                                autoHeight
                                hideFooter
                                getRowId={(row) => row.id}
                            />
                        </Grid>
                        <Grid item xs={6}>
                            <Typography variant="h6">Top 3 Most Changed Files</Typography>
                            <DataGrid
                                rows={most_frequently_changed_files_rows}
                                columns={most_frequently_changed_files_columns}
                                autoHeight
                                hideFooter
                                getRowId={(row) => row.id}
                            />
                        </Grid>
                    </Grid>
                </AccordionDetails>
            </Accordion>
        </div>
    );
};

export default Heatmap_Card_Repo;
