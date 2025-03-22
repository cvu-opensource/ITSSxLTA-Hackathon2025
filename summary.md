# Microservices and Serverless

## Microservices

> `Description:` Architectural style that structures an application as a **collection of small, independent services**, each designed to perform a specific function

- Many **loosely coupled** and **independently deployable** services
    - Each have their own technology stack
    - Eg. Database, Data management
- Allows for independent updates to codes of **different languages and stacks**
    - Better to have horizontal scaling (adding more instances of resources)
- Eg. **User Service** (Manages user accounts and authentication), **Product Service** (Handles product listings, details, and inventory), **Order Service** (Processes orders and manages order history)

- *Note:* Not to be confused with Service-Oriented Architecture (SOA)
    - Focuses on integrating large, complex systems through services that communicate over a network

### Microservices Patterns

1. **Single-Page Application (SPA)**
    - **Purpose**: To create a seamless user experience by loading a single HTML page and dynamically `updating content without reloading the page`
    - **Use Case**: Applications that require fast interactions (eg. web apps that need to respond quickly to user input)

2. **Backend for Frontend (BFF)**
    - **Purpose**: To provide a `tailored backend for different user interfaces` (*eg. mobile vs web*) to optimize performance and user experience
    - **Use Case**: Application needs to serve different types of clients with specific requirements, allowing for better customization

3. **Strangler**
    - **Purpose**: To `gradually refactor a monolithic application into microservices` by replacing parts of the old system with new microservices over time
    - **Use Case**: For managing legacy systems, allowing for a smooth transition without complete system downtime

4. **Service Discovery**
    - **Purpose**: To `enable services to find and communicate with each other dynamically`, especially in environments where services can change frequently
    - **Use Case**: Essential in microservices architectures to manage service instances that may scale or fail

### Why Microservices?

- Small Applications
    - **Simplify maintenance and management, Scalability and Speed**
    - vs Monolithic structures: Difficult to maintain

### Why NOT Microservices?

- Going too far with the 'micro' in microservices can result in **NANOservices** with over-complexity
- Building microservices without proper deployment and monitoring or cloud services is asking for unnecessary trouble

## Serverless

> `Description:` Cloud computing execution model where the **cloud provider dynamically manages the allocation of machine resources**
>
> Describes a finer-grain deployment model where applications (bundled as one or more functions) are uploaded to a platform<br>
> and then executed, scaled and biled **in response to the exact demand** needed at that moment

<img src='static/Serverless_architecture.png' width=400px>

- A combination of FaaS (Function-as-a-Service) and Baas (Backend-as-a-Service)
- They have the following characteristics;
    1. **Hostless** (developers do not have to manage or maintain server)
    2. **Elastic** (auto-scaling is automatic and inherent)
    3. **Load-balanced** (distributes incoming traffic across multiple backend systems)
    4. **Stateless** 
    5. **Event-driven** (functions only triggered when events occur)
    6. **Highly available**
    7. **Usage-based**
- Examples
    - Microsoft Azure
    - AWS Lambda
    - IBM Cloud
    - Knative

### How serverless functions work

1. **Function Creation:**

    - Developers **write code** in a supported programming language (e.g., Python, Java, Node.js).
    - The code is packaged as a function, which performs a specific task

2. **Deployment:**

    - The function is **uploaded to a cloud provider's serverless platform** (e.g., AWS Lambda, Azure Functions)
    - The cloud provider handles the infrastructure, scaling, and management

3. **Event Triggering:**
    - The function is **set to respond to specific events**, such as;
        - HTTP requests (e.g., a user clicks a button on a web app)
        - Changes in a database (e.g., a new record is added)
        - Scheduled events (e.g., running a function every hour)

4. **Execution:**
    - When the specified event occurs, the cloud provider automatically invokes the function.
    - The function **runs in a stateless environment**, meaning it does not retain any data between executions

5. **Scaling:**
    - The cloud provider automatically scales the function based on demand
    - If multiple events occur simultaneously, multiple instances of the function can run concurrently

6. **Billing:**
    - Users are **billed based on the actual compute time used** during the function's execution, rather than for idle server time

### Serverless Framework

> `Description:` Simplifies building, deploying, and managing serverless applications by abstracting infrastructure provisioning.
>
> Supports multiple cloud providers like AWS, Azure, and Google Cloud.<br>
> Allows developers to define serverless functions and associated infrastructure using simple configuration files

#### Implementing with yaml example (AWS lambda function triggered by HTTP request)
```yml
service: my-service

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1

functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: hello
          method: get
```

### FaaS (Function-as-a-Service)

> `Description:` Cloud computing service that allows you to execute code in response to events without managing the underlying infrastructure
>
> `Note:` It is a subset of serverless computing

- Creates applications as functions
- Characteristics:
    - Stateless: Each function is independent and does not retain state between executions.
    - Event-driven: Functions are triggered by events, such as HTTP requests or scheduled jobs.
    - Scalable: Functions can scale automatically based on demand.
    - Cost-effective: You only pay for the execution time of the functions, not for idle server time.
- Examples:
    - Image Processing
        - User uploads a profile picture to a website
        - Upload triggers a FaaS function that processes the image (e.g., creating a th     umbnail) and stores it in an object storage service
    - Data Processing:
        - A new record is added to a database
        - Event triggers a FaaS function that processes the data, performs calculations, or sends notifications based on the new entry

## WSGI vs ASGI
### Web Server Gateway Interface (WSGI)

> `Description:` Specification that defines a standard interface between web servers and Python web applications or frameworks

1. Synchronous Communication
    - Designed for synchronous applications, meaning it handles one request at a time
    - Leads to blocking behavior if a request takes a long time to process

2. Two Main Components
    - Server
        - The web server (like Apache or Nginx) that receives HTTP requests and forwards them to the WSGI application
    - Application
        - The Python application that processes the request and returns a response

3. Standardized Interface
    - Provides a standard interface that allows developers to write web applications that can run on any WSGI-compliant server
    - Promotes portability and flexibility

4. Request and Response Handling
    - WSGI application is a callable (like a function) that takes two arguments:
        - environ
            - Dictionary containing request information (e.g., request method, headers, and path)
        - start_response
            - Callback function used to send the HTTP status and headers back to the server

### Asynchronous Server Gateway Interface (ASGI)

> `Description:` Specification that allows for asynchronous communication between web servers and Python web applications
>
> `Why Python?`<br>
> ASGI leverages features like `async` and `await` in python to handle multiple requests concurrently.<br>
> Many popular python frameworks like `Django` and `FastAPI` work with ASGI too.

1. Asynchronous Communication
    - Essential for handling multiple requests simultaneously without blocking
    - Particularly useful in microservices architectures where services need to communicate efficiently

2. Serverless Applications
    - Can be used to build applications that respond to events (like HTTP requests) without managing the underlying infrastructure
    - Aligns with the serverless model, where you focus on writing code while the platform handles scaling and deployment

3. Microservices
    - Microservices often require lightweight, efficient communication between services
    - ASGI facilitates this by allowing services to handle requests asynchronously, improving performance and responsiveness
---
### Why serverless?

- Ability to run applications without managing underlying infrastructure
- Requires only serverless structure for core code
- Apps are deployed quickly and free up resources when not in use
- Pay as you go 

### Why NOT serverless?

- Dependency on service provider's technology, security and languages available
- Idle periods lead to increased function run time, making it unsuitable for time-critical applications
- Local cache only lasts certain hours so no data persistency

### Serverless vs Containers

| **Feature**          | **Traditional Computing**                       | **Serverless Computing**                        | **Container Computing**                        |
|----------------------|-------------------------------------------------|-------------------------------------------------|-----------------------------------------------|
| **Deployment**       | Manual setup of servers and infrastructure.     | Deploy code without managing servers.           | Package applications with dependencies into containers. |
| **Portability**      | Low; tied to specific hardware or OS.           | Low; depends on the cloud provider's ecosystem. | High; containers are portable across platforms. |
| **Latency**          | Consistent, but depends on resource allocation. | May experience cold starts.                     | Low; containers start quickly and run efficiently. |
| **Scalability**      | Manual provisioning of resources.               | Auto-scaled by the provider.                    | Scaled manually or via orchestration tools.    |
| **Cost**             | Fixed; pay for unused resources.                | Pay-as-you-go; costs scale with usage.          | Cost-efficient; pay only for running containers. |
| **Complexity**       | High; manage servers, OS, and networking.       | Low; infrastructure abstracted by the provider. | Moderate; requires managing container infrastructure. |
| **Use Cases**        | Long-running, resource-heavy apps.              | Event-driven workloads and lightweight APIs.    | Portable apps, CI/CD pipelines, microservices. |
| **Examples**         | AWS EC2, on-prem servers.                       | AWS Lambda, Google Cloud Functions.             | Docker, Kubernetes, AWS ECS/EKS.              |


## Twelve-Factor App Methodology

The methodology helps create efficient web applications, often delivered as services.<br>
There are **code** factors, **deployment** factors and **operation** factors that provide insights.

### Some key points include;
- **Codebase**: Maintain a single codebase for an app, tracked in a version control system.

- **Build, Release, Run**: Separate these stages to ensure code integrity.

- **Dev/Prod Parity**: Minimize differences between development and production environments.

- **Dependencies**: Explicitly declare all dependencies to ensure reliability.

- **Configuration**: Use environment variables for deployment-specific configurations.

- **Processes**: Keep processes stateless (*each request contains all the information required to process it*) and share nothing.

- **Concurrency**: Scale applications by running concurrent processes.

- **Disposability**: Ensure quick startup and graceful termination of processes.

- **Logs**: Handle logs as a stream of events, not stored by the application.

- **Admin Processes**: Include one-off processes for managing the app.

## Service Mesh

> `Description:` Dedicated layer that **enables fast, secure and reliable service-to-service-communication**<br>
>
> Plays a crucial role in managing communication between microservices and can complement serverless architectures

- Manages traffic between services
- Encrypts traffic between services
- Observe behavior of service to troubleshoot and optimise 
- Eg. Istio

---
---

<br>

# REST (REpresentational State Transfer)

> `Description:` Architectural style for **designing networked applications**. <br>
> 
> It defines a set of **constraints and properties based on HTTP**, which allows different components of an application to communicate with each other in a stateless manner

- This means that REST is an adjective to describe APIs
    - There are other types of APIs (aside from REST) including SOAP (Simple Object Access Protocol) and GraphQL
- `We will use RESTful APIs to handle how microservices communicate with each other`

### Characteristics of RESTful APIs

1. **HTTP Methods**
    - Uses **standard HTTP methods like POST, GET, PUT, and DELETE** for CRUD operations

2. **Stateless cleint-server Communication**
    - Each request from the client to the server **must contain all the information needed** to understand and process the request
        - Cannot take advantage of any stored context on server
        - Session state is fully on the client

3. **Uniform Interface**
    - Resources are identified by Uniform Resource Identifier (URIs), and the same data should be accessible through a consistent interface
        - Regardless of where the request originates

### Making API requests using cURL and Postman

`cURL (Client URL):` **Command-line tool** for transferring data using various network protocols (e.g., HTTP, HTTPS, FTP)
- allows you to make HTTP requests directly from the command line or scripts
    ```
    bash
    curl -X GET -H "Accept: application/json" http://example.com/api/products
    ```

`Postman:` **API platform** that provides a user-friendly interface for building, testing, and documenting APIs
- simplifies the API lifecycle by allowing users to orchestrate multiple requests and collaborate easily

## API Gateways

> `Description:` API management tool that sits between client and collection of backend services

- Managed Gateways eg. IBM DataPower Gateway, Google Apigee, Microsoft Azure, Amazon
- Open source Gatewats eg. Kong, Apache APISIX

### Why use API gateways?

- Protects APIs from mallicious usage or overuse (rate limiting)
- Analyze and monitor API usage 
- Monetize APIs
- Provides a single point of contact to microservices and simplifies client interactions
    - Fewer requests to backend with unified access to APIs
- Allows seamless addition/removal/replacement of APIs

### Why NOT use API gateways?

- Requires maintenance
- May increase response time

## Documenting APIs with Swagger

> `Description:` Tool used for **documenting and testing** REST APIs

- **API Documentation**
    - Swagger provides a standardized way to describe the structure and functionality of APIs, making it easier for developers to understand how to use them
- **OpenAPI Specification (OAS)**
    - It adheres to the OpenAPI Specification (A language-agnostic format for defining RESTful APIs)
        - Includes info on available endpoints, operations on each endpoint, operation parameters, input and output for each operation, authentication methods, contact information, license, terms of use, and other information
- **Interactive UI** 
    - Swagger generates an interactive user interface that allows users to test API endpoints directly from the documentation

## GraphQL

> `Description:` **Query language for APIs** that allows clients to request only the data they need

### GraphQL vs REST
| Feature            | GraphQL                                | REST                 |
| ------------------ | -------------------------------------- | -------------------- |
| **Endpoint**       | Single                                 | Multiple             |
| **Data Retrieval** | Clients specify exactly what they need | Fixed data structure |

#### Graphql Example
```graphql
INPUT
{
    user(id: "1"),
    {
        name
        email
    }
}
```
```json
OUTPUT
{
  "user": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```
#### REST Example
```cURL
INPUT
GET /users/1
```
```json
OUTPUT
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "address": "123 Main St"
}
```
---
---

<br>

# IBM Cloud Code Engine

> `Description:` Provides a serverless environment that simplifies the deployment and management of applications, including microservices
>
>  3 main use cases: 1) deploy applications, 2) build and deploy applications, and 3) run jobs

- **No Infrastructure Management**
    - Developers do not need to manage the underlying servers or infrastructure
    - Simply deploy code, and the platform takes care of the rest
- **Automatic Scaling**
    - Automatically scales applications up or down based on demand
    - During peak times, it can handle more requests, and vice versa
- **Focus on Code**
    - Developers can concentrate on writing and deploying their applications without worrying about server configurations, maintenance, or scaling issues

### Using IBM Cloud Code Engine

1. Create an IBM Cloud Account and access IBM Cloud Code Engine
    -  Log in to your IBM Cloud account
    - Navigate to the Code Engine service from the IBM Cloud dashboard
2. Create a New Application
    - Click on Create to start a new application
    - You can choose to deploy from a Container image or Source code
3. Deploying...
    - From a Container Image
        - If you select a container image, provide the image reference and any necessary registry access
        - Click Create to deploy the application
    - From Source Code
        - Specify a Dockerfile or buildpack along with your code
        - Follow the prompts to configure your application settings
4. Testing Your Application
    - Once deployed, you will receive an endpoint URL to test your application
5. Using IBM Cloud CLI (optional)
    - If you prefer command line, you can use the IBM Cloud CLI
    - Use commands like ibmcloud ce app create to create and deploy your application

### Command to deploy a microservice 

- Cloning and navigating project
    ```CLI
    git clone <github project>
    cd <project directory>
    ```
- Deploying microservice
    ```CLI
    ibmcloud ce app create --name <directory> --image us.icr.io/${SN_ICR_NAMESPACE}/<image directory> --registry-secret icr-secret --port <port number> --build-context-dir listing --build-source <github link or '.' for current directory>
    ```
- To get URL endpoint
    ```CLI
    ibmcloud ce app get -n listing
    ```

## Updating deployed applications 

We need to update applications when;
1. **Update Environment Variables**
    - Change settings like database locations or secret keys.
2. **Update Application Visibility**
    - Modify the accessibility of your application (public, private, or project-only).
3. **Update Application Image Reference**
    - Change the container image or GitHub repository used by the application.
4. **Update Runtime Resources**
    - Adjust CPU, memory, and storage based on application needs.

#### We can use the IBM Cloud Code Engine Console or CLI to update accordingly

- Updating environment variables with CLI
    ```bash
    ibmcloud ce app update <app_name> --env <var_name>=<value>
    ```
- Updating visibility with CLI
    ```bash
    ibmcloud ce app update <app_name> --visibility <visibility_type>
    ```
---
---

<br>

# Red Hat Openshift

> `Description:` Hybrid cloud, enterprise **Kubernetes application platform** that supports both on-premises and cloud environments to **run containerized workloads** (eg. microservices)
> 
> **Builds on Kubernetes**, similar to how various Linux distributions (eg. ubuntu, debian, fedora) build on the Linux kernel.<br>
> Designed for running microservices and can integrate with serverless technologies. <br>
>
> `Note:` Platform-as-a-Service (PaaS)

### How does it work?

- Kubernetes
    - Built on Kubernetes, which manages containerized applications across a cluster of machines
- Containers
    - Applications are packaged in containers, ensuring consistency across different environments
- Image Registry
    - Includes a built-in image registry for storing and managing container images

#### Steps to use
1. Project Creation
    - Developers create a project in OpenShift to organize their applications and resources
2. Application Deployment
    - Using the OpenShift CLI or web console, developers deploy applications by specifying container images and configurations
3. Continuous Integration/Continuous Deployment (CI/CD)
    - OpenShift automates the build and deployment process
        - Eg. when code is pushed to a repository (like GitHub), it triggers a Jenkins job that builds a new container image and deploys it
4. Scaling
    - Automatically scale applications based on demand, ensuring optimal resource usage
5. Monitoring and Management
    - Tools for monitoring application performance and managing resources effectively