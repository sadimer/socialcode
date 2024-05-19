<?php

CModule::IncludeModule('iblock');

use Bitrix\Main\Web\HttpClient;
use Bitrix\Iblock\PropertyEnumerationTable;

function parseJsonFromUrl($url) {
	$httpClient = new HttpClient();
	$response = $httpClient->get($url);

	if ($response === FALSE) {
		die('Error occurred');
	}

    $dataArray = json_decode($response, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("JSON decode error: " . json_last_error_msg());
    }

    foreach ($dataArray as $dataObject) {
        $el = new CIBlockElement;
        $PROP = array();
        if ($dataObject['Телефон'] !== null) {
            $PROP[1] = $dataObject['Телефон'];
        }
        if ($dataObject['Почта'] !== null) {
            $PROP[241] = $dataObject['Почта']; // CODE
        }
        if ($dataObject['Сумма'] !== null) {
            $PROP[4] = $dataObject['Сумма'];
        } else {
            $PROP[4] = 0;
        }
        if ($dataObject['Тип'] !== null) {
			$propertyId = 8;

			$propertyEnums = PropertyEnumerationTable::getList([
				'select' => ['ID', 'XML_ID', 'VALUE'],
				'filter' => ['PROPERTY_ID' => $propertyId]
			]);

			$enumValues = [];
			$flId = null;

			while ($enum = $propertyEnums->fetch()) {
				if ($enum['VALUE'] == $dataObject['Тип']) {
					$flId = $enum['ID'];
					break;
				}
				$enumValues[$enum['XML_ID']] = [
					'ID' => $enum['ID'],
					'VALUE' => $enum['VALUE']
				];
			}
			if ($flId !== null) {
				$PROP[8] = $flId;
			}
        }
        if ($dataObject['ФИО'] === null) {
            $name = $dataObject['Плательщик'];
        } else {
			$name = $dataObject['ФИО'];
		}


        $patientID = null;
        $b24ID = null;
        foreach ($dataObject['Пациент'] as $patient) {
            $patientFilter = [
				"IBLOCK_ID" => 56,
				"%NAME" => $patient
			];
            $patientRes = CIBlockElement::GetList([], $patientFilter, false, false, ["ID", "PROPERTY_B24_ID", "NAME"]);
            if ($patientObj = $patientRes->Fetch()) {
                $patientID = $patientObj['ID'];
                $patientName = $patientObj['NAME'];
                $b24ID = $patientObj['PROPERTY_B24_ID_VALUE'];
                break;
            }
        }

        $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' || $_SERVER['SERVER_PORT'] == 443) ? "https://" : "http://";
		$host = $_SERVER['HTTP_HOST'];
		$siteUrl = $protocol . $host;

        if ($patientID !== null) {
            $fundraiserFilter = ["IBLOCK_ID" => 57, "ACTIVE" => "Y", "PROPERTY_PATIENT" => $patientID];
            $fundraiserRes = CIBlockElement::GetList([], $fundraiserFilter, false, false, ["ID", "NAME", "PROPERTY_194", "PROPERTY_B24_ID", "DETAIL_PAGE_URL", "CODE"]);
            if ($fundraiserObj = $fundraiserRes->Fetch()) {
                $PROP[10] = $fundraiserObj['PROPERTY_194_VALUE'];
                $PROP[9] = $patientName;
                $PROP[236] = $fundraiserObj['PROPERTY_B24_ID_VALUE'];
                $PROP[234] = $fundraiserObj['NAME'];
                $PROP[235] = $siteUrl . str_replace("#ELEMENT_CODE#", $fundraiserObj['CODE'], $fundraiserObj['DETAIL_PAGE_URL']);;
                $PROP[238] = $b24ID;
            }
        }

        if ($dataObject['Цель'] !== null) {
			$fundraiserFilter = ["IBLOCK_ID" => 57, "ACTIVE" => "Y", "PROPERTY_194" => $dataObject['Цель']];
            $fundraiserRes = CIBlockElement::GetList([], $fundraiserFilter, false, false, ["ID", "NAME", "PROPERTY_PATIENT", "PROPERTY_194", "PROPERTY_B24_ID", "DETAIL_PAGE_URL", "CODE"]);
            if ($fundraiserObj = $fundraiserRes->Fetch()) {
                $PROP[10] = $fundraiserObj['PROPERTY_194_VALUE'];
                $PROP[236] = $fundraiserObj['PROPERTY_B24_ID_VALUE'];
                $PROP[234] = $fundraiserObj['NAME'];
                $PROP[235] = $siteUrl . str_replace("#ELEMENT_CODE#", $fundraiserObj['CODE'], $fundraiserObj['DETAIL_PAGE_URL']);
                $patientFilter = [
					"IBLOCK_ID" => 56,
					"PATIENT_VALUE" => $fundraiserObj["PROPERTY_PATIENT_VALUE"]
				];
				$patientRes = CIBlockElement::GetList([], $patientFilter, false, false, ["ID", "PROPERTY_B24_ID", "NAME"]);
				if ($patientObj = $patientRes->Fetch()) {
					$PROP[238] = $patientObj['PROPERTY_B24_ID_VALUE'];
					$PROP[9] = $patientObj['NAME'];
				}
            }
		}

        $filter = [
            "IBLOCK_ID" => 4,
            "PROPERTY_238" => $PROP[238],
            "PROPERTY_235" => $PROP[235],
            "PROPERTY_234" => $PROP[234],
            "PROPERTY_238" => $PROP[238],
            "PROPERTY_236" => $PROP[236],
            "PROPERTY_10" => $PROP[10],
            "PROPERTY_9" => $PROP[9],
            "PROPERTY_4" => $PROP[4],
            "NAME" => $name,
        ];
        $existingRequest = CIBlockElement::GetList([], $filter, false, false, ["ID"])->Fetch();

        if ($existingRequest) {
            continue;
        }

        $arLoadProductArray = Array(
            "MODIFIED_BY"    => 7, // $USER->GetID(), // Работает только в крон джобе
            "IBLOCK_SECTION_ID" => false,
            "IBLOCK_ID"      => 4,
            "PROPERTY_VALUES"=> $PROP,
            "NAME"           => $name,
            "ACTIVE"         => "Y",
        );
        if($PRODUCT_ID = $el->Add($arLoadProductArray)) {
            echo "New ID: ".$PRODUCT_ID;
        } else {
            echo "Error: ".$el->LAST_ERROR;
        }
    }
}

?>
