


GENERAL_TENANCY_INFO = {
    "notice_periods": {
        "info": "Most jurisdictions require 30-60 days notice from both landlords and tenants before ending a lease.",
        "clarification": "Specific notice periods vary by location and lease terms."
    },
    "security_deposits": {
        "info": "Security deposits typically must be returned within 14-30 days after move-out, minus valid deductions.",
        "clarification": "Landlords usually must provide itemized lists of deductions."
    },
    "repairs": {
        "info": "Landlords are generally responsible for maintaining habitable conditions and essential services.",
        "clarification": "Tenants usually must promptly report issues and allow reasonable access for repairs."
    },
    "rent_increases": {
        "info": "Most jurisdictions limit how often and by how much rent can be increased.",
        "clarification": "Notice periods for rent increases commonly range from 30-90 days."
    },
    "eviction": {
        "info": "Legal eviction requires proper notice, valid cause, and court procedures in most regions.",
        "clarification": "Self-help evictions (changing locks, removing belongings, utility shutoffs) are typically illegal."
    }
}


REGION_SPECIFIC_INFO = {
    "USA": {
        "general": "Housing laws vary significantly by state and sometimes city in the US.",
        "security_deposit": "Most states limit security deposits to 1-2 months' rent and specify return periods of 14-60 days.",
        "eviction": "Most states require written notice (3-30 days depending on cause) before filing for eviction."
    },
    "UK": {
        "general": "The UK has specific protections under the Housing Act and requires deposit protection schemes.",
        "security_deposit": "Deposits must be protected in government-approved schemes within 30 days of receipt.",
        "eviction": "Section 21 (no-fault) and Section 8 (with cause) notices are the two main eviction procedures."
    },
    "Canada": {
        "general": "Tenancy laws are primarily provincial rather than federal.",
        "security_deposit": "Most provinces limit deposits to half a month or one month's rent.",
        "eviction": "Each province has specific notice periods and valid reasons for eviction."
    },
    "Australia": {
        "general": "Each state and territory has its own Residential Tenancies Act.",
        "security_deposit": "Bond amounts are typically limited to 4-6 weeks of rent and must be lodged with the relevant bond authority.",
        "eviction": "Notice periods vary by state but typically range from 14-60 days depending on circumstances."
    }
}


COMMON_QUESTIONS = {
    "deposit": {
        "question": "When should I get my security deposit back?",
        "answer": "Typically within 14-30 days after move-out, but this varies by location. Landlords usually must provide itemized deductions."
    },
    "notice": {
        "question": "How much notice do I need to give before moving out?",
        "answer": "Usually 30-60 days for month-to-month leases, or as specified in your lease agreement. Written notice is typically required."
    },
    "repairs": {
        "question": "Who is responsible for repairs in my rental?",
        "answer": "Landlords are generally responsible for maintaining the property in habitable condition. This includes structural elements, plumbing, heating, and electrical systems. Tenants are typically responsible for minor maintenance and damage they cause."
    },
    "rent_increase": {
        "question": "Can my landlord raise the rent anytime?",
        "answer": "No. Most jurisdictions require proper notice (often 30-90 days) and limit frequency (typically once per year). Some areas have rent control that limits the amount of increases."
    },
    "eviction": {
        "question": "Can my landlord evict me without notice?",
        "answer": "No. Legal evictions require proper written notice, valid cause, and court procedures in most places. The notice period varies by location and situation, but immediate evictions without process are generally illegal."
    }
}

def get_region_info(region):
    """Get region-specific tenancy information"""
    region = region.upper()
    if region in REGION_SPECIFIC_INFO:
        return REGION_SPECIFIC_INFO[region]
    return None

def get_general_tenancy_info():
    """Get general tenancy information"""
    return GENERAL_TENANCY_INFO

def get_common_question_answer(topic):
    """Get a common question and answer by topic"""
    topic = topic.lower()
    if topic in COMMON_QUESTIONS:
        return COMMON_QUESTIONS[topic]
    return None