# gitlab-mirror-merge-request-resource
A concourse resource that mirrors merge requests.
An example on how this can be useful is a workflow where approved merge request that pass multiple stages in one branch gets open automatically for the production branch so that can be cherry picked by the senior dev team for delivery.