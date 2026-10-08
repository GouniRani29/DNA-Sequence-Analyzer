import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8080"
});

export const analyzeDNA = async (sequence) => {
  const response = await API.post("/analysis", {
    sequence: sequence
  });

  return response.data;
};

export const getAllAnalyses = async () => {
  const response = await API.get("/analysis");
  return response.data;
};

export const getAnalysisById = async (id) => {
  const response = await API.get(`/analysis/${id}`);
  return response.data;
};

export const deleteAnalysis = async (id) => {
  const response = await API.delete(`/analysis/${id}`);
  return response.data;
};