import logging
import requests
from odoo import fields, models

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    maaa_no = fields.Char(string='MAAA No.')
    business_name = fields.Char(string='Business Name')
    mob = fields.Char(string='Mobile')
    portal_email = fields.Char(string='Portal Email')
    portal_reg_no = fields.Char(string='Portal Registration No.')
    supplier_number = fields.Char(string='Supplier Number')
    supplier_type_name = fields.Char(string='Supplier Type')
    supplier_sub_classification = fields.Char(string='Supplier Sub Classification')
    supplier_sub_type_name = fields.Char(string='Supplier Sub Type')
    government_type_name = fields.Char(string='Government Type')
    id_type_name = fields.Char(string='ID Type')
    country_of_origin_name = fields.Char(string='Country of Origin')
    business_status_name = fields.Char(string='Business Status')
    industry_classification_name = fields.Char(string='Industry Classification')
    legal_name = fields.Char(string='Legal Name', store=True)
    trading_name = fields.Char(string='Trading Name')
    sa_company_number = fields.Char(string='SA Company Number')
    registration_date = fields.Date(string='Registration Date')
    contact_name = fields.Char(string='Contact Name')
    contact_surname = fields.Char(string='Contact Surname')
    contact_email = fields.Char(string='Contact Email')
    contact_cell_no = fields.Char(string='Contact Cell No.')
    contact_sa_id_no = fields.Char(string='Contact SA ID No.')
    bank_account_holder_name = fields.Char(string='Bank Account Holder Name')
    bank_account_type = fields.Selection([
        ('current', 'Current'),
        ('savings', 'Savings'),
        ('business', 'Business')
    ], string='Bank Account Type')
    bank_name = fields.Char(string='Bank Name')
    bank_branch_name = fields.Char(string='Bank Branch Name')
    bank_branch_number = fields.Char(string='Bank Branch Number')
    bank_account_number = fields.Char(string='Bank Account Number')
    income_tax_number = fields.Char(string='Income Tax Number')
    vat_number = fields.Char(string='VAT Number')
    paye_number = fields.Char(string='PAYE Number')
    tax_clearance_certificate_expiry_date = fields.Date(string='Tax Clearance Certificate Expiry Date')
    tax_status = fields.Selection([
        ('valid', 'Valid'),
        ('expired', 'Expired')
    ], string='Tax Status')
    director_name = fields.Char(string='Director Name')
    director_surname = fields.Char(string='Director Surname')
    director_sa_id_no = fields.Char(string='Director SA ID No.')
    director_appointment_date = fields.Date(string='Director Appointment Date')
    director_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Director Status')
    director_type = fields.Selection([
        ('executive', 'Executive'),
        ('non_executive', 'Non-Executive')
    ], string='Director Type')
    director_ownership_percent = fields.Float(string='Director Ownership Percent')
    municipality = fields.Char(string='Municipality')
    addr_line1 = fields.Char(string='Address Line 1')
    addr_line2 = fields.Char(string='Address Line 2')
    suburb = fields.Char(string='Suburb')
    preferred_contact_name = fields.Char(string='Preferred Contact Name')
    preferred_contact_email = fields.Char(string='Preferred Contact Email')
    preferred_contact_phtype = fields.Selection([
        ('phone', 'Phone'),
        ('email', 'Email')
    ], string='Preferred Contact Type')
    preferred_contact_cell = fields.Char(string='Preferred Contact Cell')
    supp_name = fields.Char(string='Supplier Name')
    supp_surname = fields.Char(string='Supplier Surname')
    supp_cellno = fields.Char(string='Supplier Cell No.')
    supp_email = fields.Char(string='Supplier Email')
    bbbee_no_rating = fields.Char(string='BBBEE No. Rating')
    bbbee_start_date = fields.Date(string='BBBEE Start Date')
    bbbee_exp_date = fields.Date(string='BBBEE Expiry Date')
    bbbee_days_to_exp = fields.Integer(string='Days to Expiry')
    is_public_beneficiary = fields.Boolean(string='Public Beneficiary')
    location_evidence = fields.Many2many('ir.attachment', 'res_partner_location_evidence_rel', 'partner_id', 'attachment_id', string='Location Evidence')
    contact_evidence = fields.Many2many('ir.attachment', 'res_partner_contact_evidence_rel', 'partner_id', 'attachment_id', string='Contact Evidence')
    coida_evidence = fields.Many2many('ir.attachment', 'res_partner_coida_evidence_rel', 'partner_id', 'attachment_id', string='COIDA Evidence')
    bbbee_certificate = fields.Many2many('ir.attachment', 'res_partner_bbbee_certificate_rel', 'partner_id', 'attachment_id', string='BBBEE Certificate')

    def get_auth_token(self):
        headers = {
            "accept": "application/json",
            "content-type": "application/xml"
        }
        data_xml = '''<AuthenticationRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
               <AcceptTermsandConditions>true</AcceptTermsandConditions>
               <Email>{email_address}</Email>
               <Password>{Password}</Password>
           </AuthenticationRequest>'''

        try:
            response = requests.post("https://api.csd.gov.za/api/Authenticate", data=data_xml.encode('utf-8'), headers=headers)
            
            if response.status_code == 200:
                json_response = response.json()
                return json_response.get("Token")
            else:
                _logger.error(f"Authentication failed with status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            _logger.error(f"API request failed: {e}")
            return None

    def get_supplier_details(self, token, supplier_number):
        supplier_url = "https://api.csd.gov.za/api/Supplier/GetSupplierDetailsFull"
        
        supplier_payload = f"""<GetSupplierDetailRequest xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema'>
                                   <SupplierNumber>{supplier_number}</SupplierNumber>
                               </GetSupplierDetailRequest>"""
        
        headers = {
            'Authorization': f'Bearer {token}',  
            'Content-Type': 'application/xml'
        }

        try:
            supplier_response = requests.post(supplier_url, headers=headers, data=supplier_payload)
            
            if supplier_response.status_code == 200:
                return supplier_response.json()
            else:
                _logger.error(f"Failed to fetch supplier details: {supplier_response.status_code}")
                return None
        
        except requests.exceptions.RequestException as e:
            _logger.error(f"API request failed: {e}")
            return None

    def action_get_supplier_details(self):
     supplier_number = self.supplier_number

     if not supplier_number:
        _logger.error("Supplier number is missing.")
        return

    # Step 1: Get authentication token
     token = self.get_auth_token()

     if not token:
        _logger.error("Failed to retrieve authentication token.")
        return

    # Step 2: Fetch supplier details
     supplier_data = self.get_supplier_details(token, supplier_number)

     if not supplier_data:
        _logger.error("Failed to retrieve supplier data.")
        return

    
     supplier_identification = supplier_data.get("SupplierIdentificationDetails", {})
     supplier_contact_details = supplier_data.get("SupplierContactDetails", {})
     supplier_address_details = supplier_data.get("SupplierAddressDetails", {})
     supplier_banking_details = supplier_data.get("SupplierBankingDetails", {})
     supplier_tax_details = supplier_data.get("SupplierTaxDetails", {})
     supplier_director_details = supplier_data.get("SupplierDirectorDetails", {})
     Supplier_BBBEE_Details = supplier_data.get("SupplierBBBEEDetails", {})

     first_contact = supplier_contact_details.get("SupplierContacts", [])[0] if supplier_contact_details.get("SupplierContacts") else {}
     first_address = supplier_address_details.get("SupplierAddressList", [])[0] if supplier_address_details.get("SupplierAddressList") else {}
     first_banking = supplier_banking_details.get("BankAccountList", [])[0] if supplier_banking_details.get("BankAccountList") else {}
    
    # Writing data to the fields
     self.write({
        'legal_name': supplier_identification.get('LegalName'),
        'business_name': supplier_identification.get('BusinessName'),
        'mob': first_contact.get('CellphoneNumber'),
        'portal_email': first_contact.get('EmailAddress'),
        'portal_reg_no': supplier_identification.get('SACompanyNumber'),
        'supplier_type_name': supplier_identification.get('SupplierTypeName'),
        'supplier_sub_classification': supplier_identification.get('SupplierSubClassificationID'),
        'supplier_sub_type_name': supplier_identification.get('SupplierSubTypeName'),
        'government_type_name': supplier_identification.get('GovernmentTypeName'),
        'id_type_name': supplier_identification.get('IDTypeName'),
        'country_of_origin_name': supplier_identification.get('CountryOfOriginName'),
        'business_status_name': supplier_identification.get('BusinessStatusName'),
        'industry_classification_name': supplier_identification.get('IndustryClassificationName'),
        'trading_name': supplier_identification.get('TradingName'),
        'sa_company_number': supplier_identification.get('SACompanyNumber'),
        'registration_date': supplier_identification.get('RegistrationDate'),
        'contact_name': first_contact.get('Name'),
        'contact_surname': first_contact.get('Surname'),
        'contact_email': first_contact.get('EmailAddress'),
        'contact_cell_no': first_contact.get('CellphoneNumber'),
        'contact_sa_id_no': first_contact.get('SAIDNumber'),
        'bank_account_holder_name': first_banking.get('AccountHolder'),
        'bank_account_type': first_banking.get('BankAccountTypeName'),
        'bank_name': first_banking.get('BankName'),
        'bank_branch_name': first_banking.get('BranchName'),
        'bank_branch_number': first_banking.get('BankCode'),
        'bank_account_number': first_banking.get('AccountNumber'),
        'municipality': first_address.get('MunicipalityName'),
        'addr_line1': first_address.get('AddressLine1'),
        'addr_line2': first_address.get('AddressLine2'),
        'income_tax_number': supplier_tax_details.get('IncomeTaxNumber'),
        'vat_number': supplier_tax_details.get('VATNumber'),
        'paye_number': supplier_tax_details.get('PAYENumber'),
        'tax_clearance_certificate_expiry_date': supplier_tax_details.get('TaxClearanceCertificateExpiryDate'),
        # 'tax_status': supplier_tax_details.get('ValidationResponse'),
        'director_name': supplier_director_details.get('SupplierDirectors', [{}])[0].get('Name'),
        'director_surname': supplier_director_details.get('SupplierDirectors', [{}])[0].get('Surname'),
        'director_sa_id_no': supplier_director_details.get('SupplierDirectors', [{}])[0].get('SAIDNumber'),
        'director_appointment_date': supplier_director_details.get('SupplierDirectors', [{}])[0].get('AppointmentDate'),
        #'director_status': supplier_director_details.get('SupplierDirectors', [{}])[0].get('DirectorStatusTypeCode'),
        #'director_type': ', '.join(d.get('DirectorTypeName', '') for d in supplier_director_details.get('SupplierDirectors', [{}])[0].get('DirectorTypes', [])),
         'bbbee_no_rating': Supplier_BBBEE_Details.get('StatusLevelOfContributorName'),
         'bbbee_start_date': Supplier_BBBEE_Details.get('CertificateIssueDate'),
         'bbbee_exp_date': Supplier_BBBEE_Details.get('CertificateExpiryDate'),
         'bbbee_days_to_exp': Supplier_BBBEE_Details.get('DaysToExpiry'),
         #'is_public_beneficiary': supplier_data["PublicBeneficiaryStatus"].get('IsPublicBeneficiary'),
         'supp_name' : supplier_contact_details.get('Name'),
         'supp_surname': supplier_contact_details.get('Surname'),
         'supp_cellno': supplier_contact_details.get('CellphoneNumber'),
    })

     _logger.info(f"Supplier details populated successfully for {supplier_number}.")
    
     return {
        'type': 'ir.actions.client',
        'tag': 'reload'
    }
