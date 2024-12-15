import { Grid, Paper, Typography } from '@mui/material';
import {
  Inventory as InventoryIcon,
  LocalShipping as OrdersIcon,
  Warehouse as WarehouseIcon,
} from '@mui/icons-material';

export default function Dashboard() {
  const stats = [
    {
      title: 'Total Products',
      value: '1,234',
      icon: <InventoryIcon sx={{ fontSize: 40 }} />,
    },
    {
      title: 'Active Orders',
      value: '56',
      icon: <OrdersIcon sx={{ fontSize: 40 }} />,
    },
    {
      title: 'Warehouses',
      value: '3',
      icon: <WarehouseIcon sx={{ fontSize: 40 }} />,
    },
  ];

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={4} key={stat.title}>
            <Paper
              sx={{
                p: 3,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
              }}
            >
              {stat.icon}
              <Typography variant="h6" sx={{ mt: 2 }}>
                {stat.title}
              </Typography>
              <Typography variant="h4" color="primary">
                {stat.value}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </div>
  );
}
