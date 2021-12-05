# Database definition
This implementation, uses Postgres database engine.

## ER Diagram


## Tables
There are seven tables as follow

### organizations
```
CREATE TABLE public.organizations
(
    organization_id integer NOT NULL DEFAULT nextval('"Organizations_OrganizationID_seq"'::regclass),
    organization_name text COLLATE pg_catalog."default",
    CONSTRAINT "Organizations_pkey" PRIMARY KEY (organization_id)
)
```

### applications
```
CREATE TABLE public.applications
(
    application_id integer NOT NULL DEFAULT nextval('"Applications_ApplicationID_seq"'::regclass),
    name text COLLATE pg_catalog."default",
    CONSTRAINT "Applications_pkey" PRIMARY KEY (application_id)
)
```

### users
```
CREATE TABLE public.users
(
    user_id text COLLATE pg_catalog."default" NOT NULL,
    full_name text COLLATE pg_catalog."default",
    organization_id integer NOT NULL,
    CONSTRAINT "Users_pkey" PRIMARY KEY (user_id)
)
```

### application_users
```
CREATE TABLE public.application_users
(
    application_user_id integer NOT NULL DEFAULT nextval('"ApplicationUsers_ApplicationUsersID_seq"'::regclass),
    application_id integer NOT NULL,
    user_id text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "ApplicationUsers_pkey" PRIMARY KEY (application_user_id)
)
```

### machines
```
CREATE TABLE public.machines
(
    machine_id text COLLATE pg_catalog."default" NOT NULL,
    serial_no text COLLATE pg_catalog."default",
    operation_start_date date,
    CONSTRAINT "Machines_pkey" PRIMARY KEY (machine_id)
)
``` 

### sessions
```
CREATE TABLE public.sessions
(
    session_id text COLLATE pg_catalog."default" NOT NULL,
    user_id text COLLATE pg_catalog."default",
    machine_id text COLLATE pg_catalog."default",
    start_at timestamp without time zone,
    application_id integer,
    end_at timestamp without time zone,
    CONSTRAINT "Sessions_pkey" PRIMARY KEY (session_id)
)
```

### events
```
CREATE TABLE public.events
(
    session_id text COLLATE pg_catalog."default" NOT NULL,
    event_at time with time zone,
    event_type text COLLATE pg_catalog."default",
    payload text COLLATE pg_catalog."default",
    CONSTRAINT "Events_pkey" PRIMARY KEY (session_id)
)
```