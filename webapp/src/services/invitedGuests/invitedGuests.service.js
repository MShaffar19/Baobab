import axios from "axios";
import { authHeader } from '../base.service';

const baseUrl = process.env.REACT_APP_API_URL;
const UNKNOWN_COUNTRY = 260;

export const invitedGuestServices = {
  getInvitedGuestList,
  addInvitedGuest,
  createInvitedGuest,
  getRoles
}

const roleOptions = [
  { value: "Speaker", label: "Speaker" },
  { value: "Guest", label: "Guest" },
  { value: "Mentor", label: "Mentor" },
  { value: "Friend of the Indaba", label: "Friend of the Indaba" },
  { value: "Organiser", label: "Organiser" },
  { value: "Dignitary", label: "Dignitary" },
  { value: "Indaba X", label: "Indaba X" },
  { value: "Sponsor", label: "Sponsor" },
  { value: "Press", label: "Press" }
];

function getRoles() {
  return roleOptions;
}

function getInvitedGuestList(eventId) {
  return axios
    .get(baseUrl + "/api/v1/invitedGuestList?event_id=" + eventId, {
      headers: authHeader()
    })  
    .then(function (response) {
      return {
        form: response.data,
        error: ""
      };
    })
    .catch(function (error) {
      return {
        form: null,
        error:
          error.response && error.response.data
            ? error.response.data.message
            : error.message
      };
    });
}

function addInvitedGuest(email_address, event_Id, role) {
  let data = {
    event_id: event_Id,
    email: email_address,
    role: role,
  };
  return axios
    .post(baseUrl + "/api/v1/invitedGuest", data, { headers: authHeader() })
    .then(function (response) {
      return {
        msg: "succeeded",
        response: response
      }
    })
    .catch(function (error) {
      if (error.response && error.response.status === 404) {
        return { msg: "404" }
      }
      else if (error.response && error.response.status === 409) {
        return { msg: "409" }
      }
      else {
        return {
          msg: "Failed",
          error: (error.response && error.response.data) ? error.response.data.message : error.message,
        }
      }
    })
}


function createInvitedGuest(user, event_Id, role) {
  let data = {
    event_id: event_Id,
    email: user.email,
    firstname: user.firstName,
    lastname: user.lastName,
    user_title: user.title,
    nationality_country_id: user.nationality || UNKNOWN_COUNTRY,  
    residence_country_id: user.residence || UNKNOWN_COUNTRY, 
    user_gender: user.gender,
    affiliation: user.affiliation,
    department: user.department || " ",
    user_disability: user.disability || "none",
    user_category_id: user.category,
    user_primaryLanguage: user.primaryLanguage || null,
    user_dateOfBirth: new Date(user.dateOfBirth ? user.dateOfBirth : "1900-01-01").toISOString(),
    role: role,
  };
  return axios
    .post(baseUrl + "/api/v1/invitedGuest/create", data, { headers: authHeader() })
    .then(function (response) {

      return {
        msg: "succeeded",
        response: response
      }
    })
    .catch(function (error) {
      if (error.response && error.response.status === 409) {
        return { msg: "409" }
      } else {
        return {
          msg: "Failed",
          error: (error.response && error.response.data) ? error.response.data.message : error.message,
        }
      }
    })
}