# from app import db


# class Subscription(db.Model):
    
#   __tablename__ = "subscriptions"

#   id = db.Column(db.Integer, primary_key=True)
#   status = 
#   customer_id =
#   plan_id = 
#   starts_at =
#   ends_at =


#   CREATE TYPE subscription_status AS ENUM ('inactive', 'active', 'upgraded');

# CREATE TABLE IF NOT EXISTS subscriptions
# (
#     id BIGSERIAL PRIMARY KEY,
#     status subscription_status NOT NULL,
#     customer_id BIGINT NOT NULL,
#     plan_id BIGINT NOT NULL,
#     invoice_id BIGINT NOT NULL,
#     starts_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     ends_at timestamp with time zone,
#     renewed_at timestamp with time zone,
#     renewed_subscription_id BIGINT,
#     downgraded_at timestamp with time zone,
#     downgraded_to_plan_id BIGINT,
#     upgraded_at timestamp with time zone,
#     upgraded_to_plan_id BIGINT,
#     cancelled_at timestamp with time zone,
#     created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     deleted_at timestamp with time zone,
#     CONSTRAINT subscriptions_downgraded_to_plan_id_fkey FOREIGN KEY (downgraded_to_plan_id)
#         REFERENCES plans (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION,
#     CONSTRAINT subscriptions_invoice_id_fkey FOREIGN KEY (invoice_id)
#         REFERENCES invoices (id) MATCH SIMPLE
#         ON UPDATE NO ACTION