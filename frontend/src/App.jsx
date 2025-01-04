import './App.css'
import {  Route, Routes } from 'react-router-dom';
import HomePage from './components/shared/HomePage';
import SchedulePage from './components/shared/SchedulePage';
import CareerResultsPage from './components/shared/CareerResultsPage';

import CSManual from './components/majors/compsci/ManualCareersPage';
import CSSurvey from './components/majors/compsci/SurveyPage';
import CSElectives from './components/majors/compsci/ElectivesPage';

import CEManual from './components/majors/ce/ManualCareersPage';
import CESurvey from './components/majors/ce/SurveyPage';
import CEElectives from './components/majors/ce/ElectivesPage';

import EEManual from './components/majors/ee/ManualCareersPage';
import EESurvey from './components/majors/ee/SurveyPage';
import EEElectives from './components/majors/ee/ElectivesPage';

import EconManual from './components/majors/econ/ManualCareersPage';
import EconSurvey from './components/majors/econ/SurveyPage';
import EconElectives from './components/majors/econ/ElectivesPage';

import EcaccManual from './components/majors/ecacc/ManualCareersPage';
import EcaccSurvey from './components/majors/ecacc/SurveyPage';
import EcaccElectives from './components/majors/ecacc/ElectivesPage';

import SdsManual from './components/majors/sds/ManualCareersPage';
import SdsSurvey from './components/majors/sds/SurveyPage';
import SdsElectives from './components/majors/sds/ElectivesPage';


function App() {
  return (
      <Routes>
        <Route path="/" element={<HomePage />} />
            {/* Shared Pages */}
          <Route path="/schedule" element={<SchedulePage />} />
          <Route path="/career-results" element={<CareerResultsPage />} />

            {/* CS Pages */}
          <Route path="/compsci/manual-careers" element={<CSManual />} />
          <Route path="/compsci/survey-page" element={<CSSurvey />} />         
          <Route path="/compsci/electives" element={<CSElectives />} />

            {/* CE Pages */}
          <Route path="/ce/manual-careers" element={<CEManual />} />        
          <Route path="/ce/survey-page" element={<CESurvey />} />
          <Route path="/ce/electives" element={<CEElectives />} />


            {/* EE Pages */}
          <Route path="/ee/manual-careers" element={<EEManual />} />
          <Route path="/ee/survey-page" element={<EESurvey />} />
          <Route path="/ee/electives" element={<EEElectives />} />

            {/* Economics Pages */}
          <Route path="/econ/manual-careers" element={<EconManual />} />
          <Route path="/econ/survey-page" element={<EconSurvey />} />
          <Route path="/econ/electives" element={<EconElectives />} />

          <Route path="/ecacc/manual-careers" element={<EcaccManual />} />
          <Route path="/ecacc/survey-page" element={<EcaccSurvey />} />
          <Route path="/ecacc/electives" element={<EcaccElectives />} />

            {/* Statistics Pages */}
          <Route path="/sds/manual-careers" element={<SdsManual />} />
          <Route path="/sds/survey-page" element={<SdsSurvey />} />
          <Route path="/sds/electives" element={<SdsElectives />} />
      </Routes>
  );
}

export default App;



