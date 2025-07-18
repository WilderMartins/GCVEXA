import React, { useState, useEffect } from 'react';
import api from '../services/api';

const ReportsPage = () => {
  const [templates, setTemplates] = useState([]);
  const [schedules, setSchedules] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [templatesRes, schedulesRes] = await Promise.all([
        api.get('/reporting/templates/'),
        api.get('/reporting/schedules/')
      ]);
      setTemplates(templatesRes.data);
      setSchedules(schedulesRes.data);
    } catch (error) {
      console.error("Failed to fetch reporting data", error);
    }
  };

  return (
    <div>
      <h1>Reporting</h1>
      <hr />
      <TemplateManager templates={templates} onUpdate={fetchData} />
      <hr />
      <ScheduleManager schedules={schedules} templates={templates} onUpdate={fetchData} />
    </div>
  );
};

// Gerenciador de Templates
const TemplateManager = ({ templates, onUpdate }) => {
  const [name, setName] = useState('');
  const [includeSeverity, setIncludeSeverity] = useState(true);
  const [includeRemediation, setIncludeRemediation] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const config = {
      include_severity_summary: includeSeverity,
      include_remediation_rate: includeRemediation,
    };
    try {
      await api.post('/reporting/templates/', { name, config: JSON.stringify(config) });
      alert('Template created!');
      onUpdate();
    } catch (error) {
      alert('Failed to create template.');
    }
  };

  return (
    <section>
      <h2>Report Templates</h2>
      <ul>{templates.map(t => <li key={t.id}>{t.name}</li>)}</ul>
      <form onSubmit={handleSubmit}>
        <h3>New Template</h3>
        <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Template Name" required />
        <div><label><input type="checkbox" checked={includeSeverity} onChange={e => setIncludeSeverity(e.target.checked)} /> Include Severity Summary</label></div>
        <div><label><input type="checkbox" checked={includeRemediation} onChange={e => setIncludeRemediation(e.target.checked)} /> Include Remediation Rate</label></div>
        <button type="submit">Create Template</button>
      </form>
    </section>
  );
};

// Gerenciador de Agendamentos
const ScheduleManager = ({ schedules, templates, onUpdate }) => {
  const [name, setName] = useState('');
  const [templateId, setTemplateId] = useState('');
  const [recipients, setRecipients] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Simplificado para um schedule semanal (toda segunda às 9h)
    const schedule_config = { type: 'cron', day_of_week: 'mon', hour: 9 };
    try {
      await api.post('/reporting/schedules/', {
        name,
        template_id: parseInt(templateId),
        recipients: recipients.split(','),
        schedule_config: JSON.stringify(schedule_config)
      });
      alert('Schedule created!');
      onUpdate();
    } catch (error) {
      alert('Failed to create schedule.');
    }
  };

  return (
    <section>
      <h2>Scheduled Reports</h2>
      <ul>{schedules.map(s => <li key={s.id}>{s.name} (To: {s.recipients.join(', ')})</li>)}</ul>
      <form onSubmit={handleSubmit}>
        <h3>New Schedule</h3>
        <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Schedule Name" required />
        <select value={templateId} onChange={e => setTemplateId(e.target.value)} required>
          <option value="" disabled>Select a template</option>
          {templates.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
        </select>
        <input type="text" value={recipients} onChange={e => setRecipients(e.target.value)} placeholder="Emails (comma-separated)" required />
        <button type="submit">Create Schedule</button>
      </form>
    </section>
  );
};

export default ReportsPage;
