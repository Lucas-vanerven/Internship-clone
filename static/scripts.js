// StatusPath is a dictionary that contains the paths elements (from the SVG) for each status
const StatusPath = {
    "completed": '<path fill="rgba(0, 204, 102, 1)" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"/>',
    "processing": '<path fill="#FFD700" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/>',
    "pending": '<path fill="#808080" d="M256 0a256 256 0 1 1 0 512A256 256 0 1 1 256 0zM232 120l0 136c0 8 4 15.5 10.7 20l96 64c11 7.4 25.9 4.4 33.3-6.7s4.4-25.9-6.7-33.3L280 243.2 280 120c0-13.3-10.7-24-24-24s-24 10.7-24 24z"/>',
    "error": '<path fill="rgba(255, 87, 51, 1)" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z"/>',
}


// Creates a new job on the server
//
// This also handles the creation of the new elements of a job. After the creation of the elements
// this also sends the request to the server to combine the files.
async function createJob() {
    const form = document.querySelector('form');

    fetch('/cronBach/api/job/create', {
        method: 'POST',
        body: new FormData(form),
    }).then(response => {
        document.getElementById('file').value = '';
        document.getElementById('name').value = '';
        if (response.ok) {
            return response.json();
        } else {
            response.json().then(data => {
                alert(data.error);
            });
        }
    }).then(data => {
        let redirect_url = data['redirect_url'] //TODO define the redirect URL in the backend
        window.location.href = redirect_url;
    })


}

// Creates a new job element
//
// This function creates a new job element in the DOM. It uses the response from the server to create
// the new element.
//
// Args:
//     job_creation_response: The response from the server. This contains: id, name, generation_time, files (a dictionary of files,
//           where the key is the upload_id and the value is the filename)
function createJobElement(job_creation_response) {
    let job = document.createElement('div');
    job.id = job_creation_response.id;
    job.className = 'job block';

    let files = []
    Object.keys(job_creation_response.files).forEach(function(upload_id) {
        let file = job_creation_response.files[upload_id];
        files.push(`
            <li>
                <a href="/cronBach/api/job/uploads/${upload_id}/${file}">${file}</a>
            </li>
        `);
    });

    // Set up new block for the job
    job.innerHTML = `
        <div class="header">
            <div class="status-tooltip" title="{{ job.status.capitalize() }}">
                <svg class="status" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="20px" height="20px" data-status="pending">
                    <!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
                    <path fill="#FFD700" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/>
                </svg>
            </div>
            <h3>${job_creation_response.name}</h3>
        </div>
        <p class="time">${job_creation_response.generation_time}</p>
        <p>Combined from files:</p>
        <ul>
            ${files.join('')}
        </ul>
        <div class="actions">
            <div class="download" onclick="downloadFile('${job_creation_response.id }')" style="display: none;" title="Delete">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="24px" height="24px" fill="rgba(57, 54, 76, 1)">
                    <!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
                    <path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 242.7-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7 288 32zM64 352c-35.3 0-64 28.7-64 64l0 32c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-32c0-35.3-28.7-64-64-64l-101.5 0-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352 64 352zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/>
                </svg>
            </div>
            <br>
            <div class="delete" onclick="deleteJob('${job_creation_response.id}')" title="Delete">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="24px" height="24px"fill="rgba(255, 87, 51, 1)">
                    <!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
                    <path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"/>
                </svg>
            </div>
        </div>
    `;

    const parentElement = document.getElementById('inner-jobs')
    parentElement.insertBefore(job, parentElement.firstChild);
}


// Function to download file
//
// We could use fetch here, but it's easier to just set the window location to the download URL
// We're using window.location.href instead of fetch because we want the browser to download the file
// instead of just getting the file contents. We assume an error code will not appear here
// If it does, it will lead to a appropriate error page
function downloadFile(job_id) {
    window.location.href = '/cronBach/api/job/download/' + job_id;
}



// Function to rename job
//
// This function is called when the user clicks the rename button on a job. It prompts the user to enter a new name
// for the job. If the user cancels the prompt or enters an empty string, nothing happens. Otherwise, a PUT request
// is sent to the server to rename the job. If the request is successful, the name of the job is updated in the DOM.
// Otherwise, an alert is shown to the user.
function renameJob(job_id) {
    const newName = prompt('Enter new name');
    if (newName === null || newName === '') {
        return;
    }

    fetch('/cronBach/api/job/rename/' + job_id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: newName
        })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            alert('Failed to rename job');
        }
    })
    .then(data => {
        document.getElementById(job_id).getElementsByClassName('header')[0].getElementsByTagName('h3')[0].innerText = data.name;
    });

}


// Function to delete job
//
// This function is called when the user clicks the delete button on a job. It sends a DELETE request
// to the server to delete the job. If the request is successful, the job is removed from the DOM.
// Otherwise, an alert is shown to the user.
function deleteJob(job_id) {
    fetch('/cronBach/api/job/delete/' + job_id, {
        method: 'DELETE',
    }).then(response => {
        if (response.ok) {
            // delete job from DOM
            const job = document.getElementById(job_id);
            job.remove();
            clearInterval(intervalIds[job_id]);
        } else {
            response.json().then(data => {
                alert(data.error);
            });
        }
    })
}

// Polls the server for the status of a job
//
// It sends a GET request to the server to get the status of the job. If the request is successful, the status is
// updated in the DOM. If the status is 'completed', the download button is shown to the user. If the status is
// 'completed' or 'error', the interval is cleared and the status is no longer updated.
function updateStatus(job_id) {
    const status = document.getElementById(job_id).getElementsByClassName("status")[0];

    // If the status is already completed, we don't need to update it anymore
    // We can clear the interval and stop updating the status
    if (status.getAttribute('data-status') === 'completed') {
        clearInterval(intervalIds[job_id]);
        return;
    }

    fetch('/cronBach/api/job/status/' + job_id)
        .then(response => {
            if (response.ok) {
                return response;
            } else {
                throw new Error('Failed to get job status');
            }
        })
        .then(response => response.json())
        .then(data => {
            status.setAttribute('data-status', data.status);
            changeStatusIcon(status);
            if (data.status === 'completed') {
                document.querySelector('.download').style.display = 'block';
            }
        })
        .catch(error => {
            console.error(error);
        });
}


// Changes the status icon and capitalizes the visible status in text
function changeStatusIcon(status_elem_of_job) {
    status = status_elem_of_job.getAttribute('data-status');
    status_elem_of_job.innerHTML = StatusPath[status];

    capitalizedStatus = status.charAt(0).toUpperCase() + status.slice(1)
    parentElement = status_elem_of_job.parentElement;
    parentElement.title = capitalizedStatus;
}

// JavaScript to trigger the file input when the submit button is clicked
// This is needed to have a nice workflow; this enables javascript to execute code,
// and also leverage the select files html element
document.getElementById('uploadButton').addEventListener('click', function() {
    document.getElementById('file').click();
});
document.getElementById('file').addEventListener('change', createJob);

// Create intervals for unfinished jobs
// This will update the status of each job every 2 seconds
// The interval ids are stored using the job id as the key
// In this way we can remove them when they served their purpose
let intervalIds = {};
for (const job of document.querySelectorAll('.job')) {
    let status = job.getElementsByClassName("status")[0].getAttribute('data-status');
    if (status === 'completed' || status === 'error') {
        continue;
    }
    intervalIds[job.id] = setInterval(updateStatus, 2000, job.id);
}
