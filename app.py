{
  "project_name": "Barrier Prediction Web App for Laminated Films",
  "objective": "To predict OTR and WVTR of multi-layer laminated films based on the individual barrier properties of base films adjusted for thickness.",
  "mathematical_models": {
    "thickness_adjustment": {
      "description": "Adjusts the transmission rate based on the principle that Transmission Rate is inversely proportional to thickness (TR1 * T1 = TR2 * T2).",
      "formula": "TR_actual = TR_ref * (Thickness_ref / Thickness_actual)"
    },
    "lamination_barrier_summation": {
      "description": "Uses the series resistance model (Permeability of multi-layer structures).",
      "formula": "1 / TR_total = (1 / TR_layer1) + (1 / TR_layer2) + ... + (1 / TR_layerN)",
      "variables": {
        "TR_total": "Total transmission rate (OTR or WVTR) of the laminate",
        "TR_layerN": "Thickness-adjusted transmission rate of an individual layer"
      }
    }
  },
  "database_schema_sample": [
    {
      "material_category": "Metalized film",
      "film_name": "mPE(XE)-MDO",
      "ref_thickness_microns": 25,
      "ref_otr": 0.25,
      "ref_wvtr": 0.45,
      "unit_otr": "cc/m2.day",
      "unit_wvtr": "g/m2.day",
      "standard_otr": "ASTM D3985",
      "standard_wvtr": "ASTM F1249"
    },
    {
      "material_category": "Non-metalized film (EVOH)",
      "film_name": "LL-EVOH",
      "ref_thickness_microns": 70,
      "ref_otr": 1.0,
      "ref_wvtr": 6.0
    },
    {
      "material_category": "Base Film",
      "film_name": "MDOPE",
      "ref_thickness_microns": 25,
      "ref_otr": 2000,
      "ref_wvtr": 6.69
    }
  ],
  "app_workflow": {
    "step_1": "User defines the number of layers in the laminate.",
    "step_2": "For each layer, user selects a material from the database or enters custom OTR/WVTR and reference thickness.",
    "step_3": "User inputs the actual thickness for each layer used in the specific laminate design.",
    "step_4": "System calculates adjusted OTR/WVTR for each layer using the thickness_adjustment formula.",
    "step_5": "System calculates the final laminate barrier values using the lamination_barrier_summation formula.",
    "step_6": "Display results with reference to ASTM standards."
  },
  "ui_components": {
    "input_layer_table": {
      "columns": [
        "Layer Order",
        "Material Selection (Dropdown/Search)",
        "Thickness (microns)",
        "Manual Overwrite Toggle",
        "Manual OTR/WVTR Input"
      ]
    },
    "output_dashboard": {
      "metrics": [
        "Total Calculated Thickness",
        "Predicted OTR (ASTM D3985)",
        "Predicted WVTR (ASTM F1249)"
      ]
    }
  },
  "logic_considerations": [
    "Handle 'unknown' or 'low barrier' values where TR is very high (e.g., >2000) to avoid division by zero or infinity errors.",
    "Ensure units are consistent (e.g., all OTR in cc/m2.day and WVTR in g/m2.day).",
    "Provide a 'database lookup' feature to allow users to verify source research data used for the calculations."
  ]
}
