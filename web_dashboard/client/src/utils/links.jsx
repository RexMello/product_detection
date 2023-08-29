import React from 'react';

import { IoBarChartSharp } from 'react-icons/io5';
import { MdQueryStats } from 'react-icons/md';
import { FaWpforms } from 'react-icons/fa';
import { ImProfile } from 'react-icons/im';
import { MdAdminPanelSettings } from 'react-icons/md';

const links = [
 
  {
    text: 'Details',
    path: 'all-jobs',
    icon: <MdQueryStats />,
  },
  {
    text: 'Click Picture',
    path: 'stats',
    icon: <IoBarChartSharp />,
  },
  {
    text: 'Upload Picture',
    path: 'profile',
    icon: <ImProfile />,
  },
  
];

export default links;
