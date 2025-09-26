package tavo

import "fmt"

// JobOperations handles job-related operations
type JobOperations struct {
	client *Client
}

// ListJobs lists all jobs
func (j *JobOperations) ListJobs(params map[string]interface{}) (map[string]interface{}, error) {
	query := ""
	if params != nil {
		query = "?"
		for key, value := range params {
			if query != "?" {
				query += "&"
			}
			query += fmt.Sprintf("%s=%v", key, value)
		}
	}
	return j.client.makeRequest("GET", "/jobs"+query, nil)
}

// GetJob returns a specific job's information
func (j *JobOperations) GetJob(jobID string) (map[string]interface{}, error) {
	return j.client.makeRequest("GET", "/jobs/"+jobID, nil)
}

// CreateJob creates a new job
func (j *JobOperations) CreateJob(jobData map[string]interface{}) (map[string]interface{}, error) {
	return j.client.makeRequest("POST", "/jobs", jobData)
}

// UpdateJob updates a job's information
func (j *JobOperations) UpdateJob(jobID string, jobData map[string]interface{}) (map[string]interface{}, error) {
	return j.client.makeRequest("PUT", "/jobs/"+jobID, jobData)
}

// DeleteJob deletes a job
func (j *JobOperations) DeleteJob(jobID string) error {
	_, err := j.client.makeRequest("DELETE", "/jobs/"+jobID, nil)
	return err
}

// StartJob starts a job
func (j *JobOperations) StartJob(jobID string) (map[string]interface{}, error) {
	return j.client.makeRequest("POST", "/jobs/"+jobID+"/start", nil)
}

// StopJob stops a running job
func (j *JobOperations) StopJob(jobID string) (map[string]interface{}, error) {
	return j.client.makeRequest("POST", "/jobs/"+jobID+"/stop", nil)
}

// GetJobStatus returns the status of a job
func (j *JobOperations) GetJobStatus(jobID string) (map[string]interface{}, error) {
	return j.client.makeRequest("GET", "/jobs/"+jobID+"/status", nil)
}

// GetJobLogs returns the logs of a job
func (j *JobOperations) GetJobLogs(jobID string, params map[string]interface{}) (map[string]interface{}, error) {
	query := ""
	if params != nil {
		query = "?"
		for key, value := range params {
			if query != "?" {
				query += "&"
			}
			query += fmt.Sprintf("%s=%v", key, value)
		}
	}
	return j.client.makeRequest("GET", "/jobs/"+jobID+"/logs"+query, nil)
}
