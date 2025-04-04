# CREATE TYPE invoice_status AS ENUM ('draft', 'unpaid', 'paid');

# CREATE TABLE IF NOT EXISTS invoices
# (
#     id BIGSERIAL PRIMARY KEY,
#     status invoice_status NOT NULL DEFAULT 'unpaid'::invoice_status,
#     invoice_number integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1000 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
#     customer_id BIGINT NOT NULL,
#     email character varying(320) NOT NULL,
#     name character varying(320) NOT NULL,
#     country character varying(2) NOT NULL,
#     currency character varying(3) NOT NULL DEFAULT 'USD',
#     address1 character varying(255) NOT NULL,
#     address2 character varying(255),
#     city character varying(255) NOT NULL,
#     postal_code character varying(12) NOT NULL,
#     phone character varying(24),
#     invoice_date timestamp with time zone NOT NULL,
#     due_date timestamp with time zone NOT NULL,
#     paid_at timestamp with time zone,
#     created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     deleted_at timestamp with time zone,
#     CONSTRAINT invoices_invoice_number_key UNIQUE (invoice_number),
#     CONSTRAINT invoices_currency_fkey FOREIGN KEY (currency)
#         REFERENCES currencies (code) MATCH 