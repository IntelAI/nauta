/**
 * INTEL CONFIDENTIAL
 * Copyright (c) 2018 Intel Corporation
 *
 * The source code contained or described herein and all documents related to
 * the source code ("Material") are owned by Intel Corporation or its suppliers
 * or licensors. Title to the Material remains with Intel Corporation or its
 * suppliers and licensors. The Material contains trade secrets and proprietary
 * and confidential information of Intel or its suppliers and licensors. The
 * Material is protected by worldwide copyright and trade secret laws and treaty
 * provisions. No part of the Material may be used, copied, reproduced, modified,
 * published, uploaded, posted, transmitted, distributed, or disclosed in any way
 * without Intel's prior express written permission.
 *
 * No license under any patent, copyright, trade secret or other intellectual
 * property right is granted to or conferred upon you by disclosure or delivery
 * of the Materials, either expressly, by implication, inducement, estoppel or
 * otherwise. Any license under such intellectual property rights must be express
 * and approved by Intel in writing.
 */

import axios from 'axios';
import cookies from 'js-cookie';

const DECODE_TOKEN_ENDPOINT = '/api/experiments/list';

export function getExperiments (limitPerPage, pageNo, orderBy, order, searchBy, names, states, namespaces, types) {
  const token = cookies.get('TOKEN');
  let queryParams = {
    limit: limitPerPage || 5,
    page: pageNo || 1,
    orderBy: orderBy || '',
    order: order || '',
    searchBy: searchBy || '',
    names: Array.isArray(names) && names.length ? names : '*',
    states: Array.isArray(states) && states.length ? states : '*',
    namespaces: Array.isArray(namespaces) && namespaces.length ? namespaces : '*',
    types: Array.isArray(types) && types.length ? types : '*'
  };
  const options = {
    url: DECODE_TOKEN_ENDPOINT,
    headers: {
      'Authorization': token,
      'timezone-offset': new Date().getTimezoneOffset()
    },
    params: queryParams,
    method: 'GET'
  };
  return axios(options);
}

const EXPERIMENTS_ENDPOINT = '/api/experiments';

export function getExperimentsResources (experimentName) {
  const token = cookies.get('TOKEN');
  const options = {
    url: `${EXPERIMENTS_ENDPOINT}/${experimentName}/resources`,
    headers: {'Authorization': token},
    method: 'GET'
  };
  return axios(options);
}
