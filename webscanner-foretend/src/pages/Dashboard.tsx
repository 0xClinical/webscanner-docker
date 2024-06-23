import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import { dashboard } from '../services/api';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
import './Dashboard.css';

// 注册 chart.js 的元素
Chart.register(ArcElement, Tooltip, Legend);


const Dashboard: React.FC = () => {
  const [highSeverityData, setHighSeverityData] = useState<TypeData[]>( []);
  const [mediumSeverityData, setMediumSeverityData] = useState<TypeData[]>([]);
  const [lowSeverityData, setLowSeverityData] = useState<TypeData[]>([]);
  const [vulnerabilities, setVulnerabilities] = useState<VulnData[]>([]);
  interface TypeData {
      name: string,
      count: string
  }
  interface VulnData{
    type: string,
    name: string,
    urls: string[]
  }
  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await dashboard(); // 假设 dashboard 返回的是数据对象
        setHighSeverityData(result.highSeverity);
        setMediumSeverityData(result.mediumSeverity);
        setLowSeverityData(result.lowSeverity);
        setVulnerabilities(result.vulnerabilities);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    };
    fetchData();
  }, []);

  const createPieData = (severityData:TypeData[]) => {
    return {
      labels: severityData.map(item => item.name),
      datasets: [{
        data: severityData.map(item => item.count),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40'
        ],
        hoverBackgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40'
        ]
      }]
    };
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-content-overlay">
        <h2 className="dashboard-page-title">Dashboard</h2>
        <div className="charts-container">
          <div className="chart">
            <h3>High Severity</h3>
            <Pie data={createPieData(highSeverityData)} />
          </div>
          <div className="chart">
            <h3>Medium Severity</h3>
            <Pie data={createPieData(mediumSeverityData)} />
          </div>
          <div className="chart">
            <h3>Low Severity</h3>
            <Pie data={createPieData(lowSeverityData)} />
          </div>
        </div>
        <div className="vulnerabilities-table">
          <h3>Vulnerabilities</h3>
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Name</th>
                <th>URL</th>
              </tr>
            </thead>
            <tbody>
              {vulnerabilities.map((vul, index) => (
                <tr key={index}>
                  <td>{vul.type}</td>
                  <td>{vul.name}</td>
                  <td>
                    <ul>
                      {vul.urls.map((url, i) => (
                        <li key={i}>{url}</li>
                      ))}
                    </ul>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};


export default Dashboard;
